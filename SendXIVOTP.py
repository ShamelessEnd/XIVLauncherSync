from LogUtils import print_with_timestamp
import pyotp
import requests
import sys
import time
from XIVProcess import is_launcher_running

def send_single_xiv_otp(otp_code, timeout):
    url = "http://localhost:4646/ffxivlauncher/" + otp_code
    print_with_timestamp("attempting xivlauncher login at " + url)
    try:
        r = requests.get(url = url, timeout = timeout)
        return r.status_code == requests.codes.ok
    except:
        return False

def send_xiv_otp(otp_secret, timeout):
    launcher_timeout = 60
    while not is_launcher_running():
        time.sleep(1)
        launcher_timeout -= 1
        timeout -= 1
        if launcher_timeout <= 0 or timeout <= 0:
            print_with_timestamp("launcher failed to start")
            return False
    totp = pyotp.TOTP(otp_secret)
    for _ in range(timeout):
        otp_code = totp.now()
        if not is_launcher_running():
            print_with_timestamp("launcher died while sending otp")
            return False
        if send_single_xiv_otp(otp_code, 0.5):
            return True
        time.sleep(0.5)
    print_with_timestamp("failed to send otp")
    return False

if __name__ == '__main__':
    send_xiv_otp(str(sys.argv[1]), 20)
