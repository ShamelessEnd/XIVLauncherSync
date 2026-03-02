import time
import LaunchXIV
import XIVProcess
from SyncSNDScripts import sync_sndscripts
from SyncXIVLauncher import sync_xivlauncher
from LogUtils import print_with_timestamp

def auto_retainer_loop():
    if not XIVProcess.is_xiv_running():
        sync_xivlauncher('3')
        sync_sndscripts()
    else:
        print_with_timestamp("xiv is running")
    SLEEP_TIME = 10
    xiv_uptime = 0
    while True:
        if not XIVProcess.is_xiv_running():
            xiv_uptime = 0
            if XIVProcess.is_launcher_running():
                print_with_timestamp("xiv not running and launcher timed out - killing launcher")
                XIVProcess.kill_launcher()
            else:
                print_with_timestamp("xiv not running - launching")
                LaunchXIV.launch_xiv(3, 60, 60)
        else:
            xiv_uptime += SLEEP_TIME
            if xiv_uptime > 203600:
                print_with_timestamp("xiv failed to restart - killing xiv")
                if XIVProcess.kill_xiv():
                    xiv_uptime = 0

        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    auto_retainer_loop()
