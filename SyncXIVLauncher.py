import os
import sys
from LogUtils import print_with_timestamp
from pathlib import Path
from SyncFiles import sync_folders
from XIVSecrets import REMOTE_HOSTS_PATHS

SKIP_SET = set(['Artisan', 'AutoRetainer', 'Browsingway', 'IINACT', 'InventoryTools', 'Deliveroo', 'Lifestream', 'meshcache', 'cef-cache', 'stubs'])
REMOTE_SKIP_SET = set(['meshcache', 'cef-cache', 'stubs'])

def sync_xivlauncher(instance):
	print_with_timestamp('syncing instance: ' + instance)
	appdata = os.getenv('APPDATA')
	known_clients = set(['', '2', '3'])
	source_folder = os.path.join(appdata, 'XIVLauncher' + instance, 'pluginConfigs')
	backup_folder = os.path.join(appdata, 'XIVLauncher' + instance, 'pluginConfigs.bak')
	print_with_timestamp('source_folder: ' + source_folder)
	if instance in known_clients:
		for remote_host, remote_path in REMOTE_HOSTS_PATHS.items():
			if remote_host == os.getenv('COMPUTERNAME'):
				continue
			other_folder = os.path.join(remote_path, 'XIVLauncher' + instance, 'pluginConfigs')
			if os.path.exists(other_folder):
				print_with_timestamp("syncing remote " + remote_host + " XIVLauncher" + instance + " into local") 
				sync_folders(source_folder, other_folder, backup_folder, REMOTE_SKIP_SET)
			else:
				print_with_timestamp('remote path does not exist: ' + other_folder)
		for other in known_clients:
			if other == instance or other == '':
				continue
			print_with_timestamp("syncing XIVLauncher" + other + " into XIVLauncher" + instance) 
			other_folder = os.path.join(appdata, 'XIVLauncher' + other, 'pluginConfigs')
			sync_folders(source_folder, other_folder, backup_folder, SKIP_SET)
	else:
		print_with_timestamp('instance not found')

if __name__ == '__main__':
	sync_xivlauncher(str(sys.argv[1]) if len(sys.argv) > 1 else '')
