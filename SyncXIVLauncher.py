from LogUtils import print_with_timestamp
import os
import shutil
import sys
from pathlib import Path
from XIVSecrets import REMOTE_HOSTS_PATHS

SKIP_SET = set(['Artisan', 'AutoRetainer', 'Browsingway', 'IINACT', 'InventoryTools', 'Deliveroo', 'Lifestream', 'meshcache', 'cef-cache', 'stubs'])
REMOTE_SKIP_SET = set(['meshcache', 'cef-cache', 'stubs'])

def sync_files(source_file, other_file, backup_file, backup_folder):
	if os.path.exists(source_file):
		source_time = os.path.getmtime(source_file)
		other_time = os.path.getmtime(other_file)
		if source_time < other_time:
			print_with_timestamp(source_file + ' is outdated, copying from ' + other_file)
			if os.path.exists(backup_file):
				os.remove(backup_file)
			else:
				os.makedirs(backup_folder, exist_ok=True)
			shutil.copy2(source_file, backup_file)
			os.remove(source_file)
			shutil.copy2(other_file, source_file)
	else:
		print_with_timestamp(source_file + ' does not exist, copying from ' + other_file)
		shutil.copy2(other_file, source_file)

def sync_folders(source_folder, other_folder, backup_folder, skip_set):
	# print_with_timestamp('syncing folder ' + other_folder + ' into source ' + source_folder)
	for root, dirs, files in os.walk(other_folder):
		for filename in files:
			if Path(filename).stem in skip_set:
				continue
			source_file = os.path.join(source_folder, filename)
			other_file = os.path.join(other_folder, filename)
			backup_file = os.path.join(backup_folder, filename)
			sync_files(source_file, other_file, backup_file, backup_folder)
		for dirname in dirs:
			if dirname in skip_set:
				continue
			source_dir = os.path.join(source_folder, dirname)
			other_dir = os.path.join(other_folder, dirname)
			backup_dir = os.path.join(backup_folder, dirname)
			if os.path.exists(source_dir):
				sync_folders(source_dir, other_dir, backup_dir, skip_set)
			else:
				print_with_timestamp(source_dir + ' does not exist, copying from ' + other_dir)
				shutil.copytree(other_dir, source_dir)
		break

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
