from LogUtils import print_with_timestamp
from filelock import FileLock, Timeout
import SendXIVOTP
import subprocess
import sys
import time
from XIVProcess import get_running_xiv_pids, is_xiv_pid_running, is_launcher_running, kill_launcher
import XIVSecrets

def launch_xiv_with_lock(index, otp_timeout, launch_timeout, lockFile):
    lock = FileLock(lockFile)
    try:
        with lock.acquire(timeout=otp_timeout + launch_timeout + 60):
            return launch_xiv(index, otp_timeout, launch_timeout)
    except Timeout:
        print_with_timestamp("failed to acquire lock for launching xiv")
        return 0

def launch_xiv(index, otp_timeout, launch_timeout, auto_login=True):
    print_with_timestamp("launching xiv")
    if not kill_launcher():
        return 0
    current_pids = set(get_running_xiv_pids())
    subprocess.call(XIVSecrets.XIV_LAUNCH_COMMANDS[index], shell=True, cwd='C:\\')
    if not auto_login:
        return 0
    if not SendXIVOTP.send_xiv_otp(XIVSecrets.XIV_OTP_SECRETS[index], otp_timeout):
        print_with_timestamp("failed to send OTP")
        kill_launcher()
        return 0
    print_with_timestamp("waiting for xiv to launch")
    xiv_pid = 0
    while not xiv_pid and is_launcher_running() and launch_timeout > 0:
        time.sleep(1)
        launch_timeout -= 1
        new_pids = set(get_running_xiv_pids())
        if new_pids - current_pids:
            xiv_pid = list(new_pids - current_pids)[0]
    if xiv_pid and is_xiv_pid_running(xiv_pid):
        print_with_timestamp("xiv launched: " + str(xiv_pid))
        return xiv_pid
    else:
        print_with_timestamp("failed to launch xiv")
        kill_launcher()
        return 0

if __name__ == '__main__':
    launch_xiv(int(sys.argv[1]), 60, 300, len(sys.argv) < 3 or sys.argv[2].lower() != "false")
