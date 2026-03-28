import time
import signal
import sys
import LaunchXIV
import XIVProcess
from SyncSNDScripts import sync_sndscripts
from SyncXIVLauncher import sync_xivlauncher
from LogUtils import print_with_timestamp

def auto_retainer_loop(instance):
    pid = 0
    def signal_handler(sig, frame):
        XIVProcess.kill_xiv_pid(pid)
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    sync_sndscripts()
    sync_xivlauncher(str(instance))
    SLEEP_TIME = 10
    xiv_uptime = 0
    while True:
        if not pid or not XIVProcess.is_xiv_pid_running(pid):
            xiv_uptime = 0
            pid = 0
            if XIVProcess.is_launcher_running():
                print_with_timestamp("xiv not running and launcher timed out - killing launcher")
                XIVProcess.kill_launcher()
            else:
                print_with_timestamp("xiv not running - launching")
                pid = LaunchXIV.launch_xiv_with_lock(instance, 60, 60, "auto_retainer_loop.lock")
        else:
            xiv_uptime += SLEEP_TIME
            if xiv_uptime > 203600:
                print_with_timestamp("xiv failed to restart - killing xiv")
                if XIVProcess.kill_xiv_pid(pid):
                    xiv_uptime = 0
                    pid = 0
        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    auto_retainer_loop(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
