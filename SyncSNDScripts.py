import os
from LogUtils import print_with_timestamp
from SyncFiles import sync_folders
from XIVSecrets import REMOTE_SCRIPT_PATHS

SKIP_SET = set(['.git', 'ReadMe', '.vscode', 'ref', '.gitignore'])

def sync_sndscripts():
    local_host = os.getenv('COMPUTERNAME')
    local_path = REMOTE_SCRIPT_PATHS[local_host]
    if not os.path.exists(local_path):
        return
    for remote_host, remote_path in REMOTE_SCRIPT_PATHS.items():
        if remote_host == local_host:
            continue
        print_with_timestamp("syncing remote " + remote_path + " into " + local_path)
        sync_folders(local_path, remote_path, local_path + ".bak", SKIP_SET)

if __name__ == '__main__':
    sync_sndscripts()
