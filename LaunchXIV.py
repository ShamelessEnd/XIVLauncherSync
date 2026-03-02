from LogUtils import print_with_timestamp
import SendXIVOTP
import subprocess
import sys
import time
from XIVProcess import is_xiv_running, is_launcher_running
import XIVSecrets

def launch_xiv(index, otp_timeout, launch_timeout):
    print_with_timestamp("launching xiv")
    subprocess.call(XIVSecrets.XIV_LAUNCH_COMMANDS[index], shell=True, cwd='C:\\')
    if not SendXIVOTP.send_xiv_otp(XIVSecrets.XIV_OTP_SECRETS[index], otp_timeout):
        print_with_timestamp("failed to send OTP")
        return False
    print_with_timestamp("waiting for xiv to launch")
    while not is_xiv_running() and is_launcher_running() and launch_timeout > 0:
        time.sleep(1)
        launch_timeout -= 1
    if is_xiv_running():
        print_with_timestamp("xiv launched!")
        return True
    else:
        print_with_timestamp("failed to launch xiv")
        return False

if __name__ == '__main__':
    launch_xiv(int(sys.argv[1]), 300, 60)
