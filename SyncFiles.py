import os
import shutil
from LogUtils import print_with_timestamp
from pathlib import Path

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
