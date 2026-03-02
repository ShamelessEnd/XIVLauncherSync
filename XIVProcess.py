from LogUtils import print_with_timestamp
import psutil
import time

def is_process_running(pname):
    for p in psutil.process_iter():
        try:
            if p.name() == pname:
                return True
        except psutil.NoSuchProcess:
            continue
    return False

def is_xiv_running():
    return is_process_running("ffxiv_dx11.exe")

def is_launcher_running():
    return is_process_running("XIVLauncher.exe")

def kill_process(pname):
    for p in psutil.process_iter():
        try:
            if p.name() == pname:
                p.kill()
        except psutil.NoSuchProcess:
            continue
    timeout = 60
    while is_process_running(pname) and timeout > 0:
        time.sleep(1)
        timeout -= 1
    if is_process_running(pname):
        print_with_timestamp(f"failed to kill {pname}")
        return False
    else:
        print_with_timestamp(f"{pname} killed")
        return True

def kill_xiv():
    return kill_process("ffxiv_dx11.exe")

def kill_launcher():
    return kill_process("XIVLauncher.exe")
