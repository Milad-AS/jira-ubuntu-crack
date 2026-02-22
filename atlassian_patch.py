#! /usr/bin/python3
import os
import sys
import socket
import re
import subprocess

# Define color variables precisely to avoid NameError
_B = "\033[1m"
_f_r = "\033[31m"
_f_y = "\033[33m"
_f_g = "\033[32m"
_f_w = "\033[37m"
_f_bl = "\033[30m"
_f_b = "\033[34m"
_f_ex_y = "\033[93m"
_f_ex_r = "\033[91m"
_f_ex_g = "\033[92m"
_f_ex_w = "\033[97m"
_f_ex_b = "\033[94m" 
_b_y = "\033[43m"
_RSTALL = "\033[0m"

# Jira installation path on Ubuntu
JIRA_PATH = "/opt/atlassian/jira"

def logo():
    print(f"{_f_ex_b} _     _               _          _                      _   {_RSTALL}")
    print(f"{_f_ex_b}| |   | |             | |        | |                    | |  {_RSTALL}")
    print(f"{_f_ex_b}| | _ | |__   ___   __| |  ___  _| |_     _ __    ___  _| |_ {_RSTALL}")
    print(f"{_f_ex_b}| |/ /| '_ \ / _ \ / _` | / _ \ _   _|   | '_ \  / _ \ _   _|{_RSTALL}")
    print(f"{_f_ex_b}|   < | | | | (_) | (_| ||  __/  | |_    | | | ||  __/  | |_ {_RSTALL}")
    print(f"{_f_ex_b}|_|\_\|_| |_|\___/ \__,_| \___|  \___|(_)|_| |_| \___|  \___|{_RSTALL}")
    print(f"{_f_ex_b}                                                             {_RSTALL}")
    
def get_external_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except: return "127.0.0.1"

def get_jira_version():
    sh_path = f"{JIRA_PATH}/bin/version.sh"
    if not os.path.exists(sh_path):
        return "Not Found", "Not Found"
    
    try:
        # Give execute permission to version file
        subprocess.run(["chmod", "+x", sh_path], check=True)
        result = subprocess.run([sh_path], capture_output=True, text=True, timeout=5)
        output = result.stdout
        
        version = re.search(r"Jira Version\s+:\s+([\d.]+)", output, re.IGNORECASE)
        jvm = re.search(r"JVM Version\s+:\s+([\d._A-Za-z-]+)", output, re.IGNORECASE)
        
        v_out = version.group(1) if version else "Unknown"
        j_out = jvm.group(1) if jvm else "Unknown"
        return v_out, j_out
    except:
        return "Detection Failed", "Detection Failed"

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    logo()
    
    if not os.path.exists(JIRA_PATH):
        print(f"\n{_f_ex_r}Error: Jira folder not found at {JIRA_PATH}.{_RSTALL}")
        print(f"{_f_y}Note: If Jira is installed in a different path, change the JIRA_PATH variable in the code.{_RSTALL}")
        return

    v, jvm = get_jira_version()
    ext_ip = get_external_ip()

    print(f"\n{_B}Jira Service Information on Ubuntu:{_RSTALL}")
    print(f"Jira Version: {_f_ex_y}{v}{_RSTALL}")
    print(f"Java Version: {_f_ex_y}{jvm}{_RSTALL}")
    print(f"Server Address: {_f_ex_b}http://{ext_ip}:8080{_RSTALL}")
    
    print(f"\n{_f_w}--------------------------------------------------{_RSTALL}")
    print(f"{_B}1- Open your browser and navigate to the above address.{_RSTALL}")
    print(f"{_B}2- During the license step, find the {_f_y}Server ID{_f_w}.{_RSTALL}")
    print(f"{_B}3- Format: (XXXX-XXXX-XXXX-XXXX){_RSTALL}")
    
    while True:
        prompt = f'\n{_B}{_f_w}Please enter the Server ID: {_b_y}{_f_bl}'
        server_id = input(prompt).strip().upper()
        print(_RSTALL, end="") # Reset color after input
        
        if re.match(r"^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$", server_id):
            print(f"\n{_f_ex_g}Verified! Server ID: {server_id}{_RSTALL}")
            print(f"{_f_ex_y}Now enter the license in the Jira console.{_RSTALL}")
            break
        else:
            print(f"\n{_f_ex_r}Wrong format! Example: ABCD-1234-EFGH-5678{_RSTALL}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{_f_ex_r}Exiting program.{_RSTALL}")
        sys.exit()