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

def get_running_xiv_pids():
    pids = []
    for p in psutil.process_iter():
        try:
            if p.name() == "ffxiv_dx11.exe" and p.is_running():
                pids.append(p.pid)
        except psutil.NoSuchProcess:
            continue
    return pids

def is_xiv_pid_running(pid):
    try:
        p = psutil.Process(pid)
        return p.name() == "ffxiv_dx11.exe" and p.is_running()
    except psutil.NoSuchProcess:
        return False

def is_launcher_running():
    return is_process_running("XIVLauncher.exe")

def kill_process(pname):
    if not is_process_running(pname):
        return True
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
    
def kill_xiv_pid(pid):
    try:
        p = psutil.Process(pid)
        p.kill()
    except psutil.NoSuchProcess:
        print_with_timestamp(f"pid {pid} not found")
        return True
    timeout = 60
    while is_xiv_pid_running(pid) and timeout > 0:
        time.sleep(1)
        timeout -= 1
    if is_xiv_pid_running(pid):
        print_with_timestamp(f"failed to kill pid {pid}")
        return False
    else:
        print_with_timestamp(f"pid {pid} killed")
        return True

def kill_xiv():
    return kill_process("ffxiv_dx11.exe")

def kill_launcher():
    return kill_process("XIVLauncher.exe")
