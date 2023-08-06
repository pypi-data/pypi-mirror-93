from pathlib import Path
import subprocess
import time
import os
import signal

def launch_essentials(cfg):
    print("Initializing...")
    middleman_dir = Path(cfg["root"]) / cfg["middleman"]
    middle_exe = middleman_dir / "middleman.py"
    middle_cfg = middleman_dir / "config.toml"
    vsniffer_dir = Path(cfg["root"]) / cfg["vsniffer"]
    vsniffer_exe = vsniffer_dir / "vsniffer.py"
    vsniffer_cfg = vsniffer_dir / "config.toml"

    middle = subprocess.Popen(f"python3 {middle_exe} {middle_cfg} >> middleman.log", shell=True, preexec_fn=os.setsid)
    vsniffer = subprocess.Popen(f"python3 {vsniffer_exe} {vsniffer_cfg} >> vsniffer.log", shell=True, preexec_fn=os.setsid)

    time.sleep(0.1)

    return middle, vsniffer


def kill_essentials(middle, vsniffer):
    print("Stopping runtime...")
    os.killpg(os.getpgid(middle.pid), signal.SIGTERM)
    os.killpg(os.getpgid(vsniffer.pid), signal.SIGTERM)