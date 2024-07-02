import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import string
from itertools import product
from colorama import Fore, Style, init
import sys
import time
from datetime import datetime
import threading


init(autoreset=True)


class colors:
    CRED2 = "\33[91m"
    CBLUE2 = "\33[94m"
    CGREEN2 = "\33[92m"
    CGREEN_DARK = "\33[32m"
    CGREEN_LIGHT = "\33[92m"
    CBLUE_DARK = "\33[34m"
    ENDC = "\033[0m"

# ASCII
banner = """
  ██████ ██░ ██▓█████ ██▓    ██▓         ███████▓███▄    █▓█████▄▓█████ ██▀███  
▒██    ▒▓██░ ██▓█   ▀▓██▒   ▓██▒       ▓██   ▓██▒██ ▀█   █▒██▀ ██▓█   ▀▓██ ▒ ██▒
░ ▓██▄  ▒██▀▀██▒███  ▒██░   ▒██░       ▒████ ▒██▓██  ▀█ ██░██   █▒███  ▓██ ░▄█ ▒
  ▒   ██░▓█ ░██▒▓█  ▄▒██░   ▒██░       ░▓█▒  ░██▓██▒  ▐▌██░▓█▄   ▒▓█  ▄▒██▀▀█▄  
▒██████▒░▓█▒░██░▒████░██████░██████▒   ░▒█░  ░██▒██░   ▓██░▒████▓░▒████░██▓ ▒██▒
▒ ▒▓▒ ▒ ░▒ ░░▒░░░ ▒░ ░ ▒░▓  ░ ▒░▓  ░    ▒ ░  ░▓ ░ ▒░   ▒ ▒ ▒▒▓  ▒░░ ▒░ ░ ▒▓ ░▒▓░
░ ░▒  ░ ░▒ ░▒░ ░░ ░  ░ ░ ▒  ░ ░ ▒  ░    ░     ▒ ░ ░░   ░ ▒░░ ▒  ▒ ░ ░  ░ ░▒ ░ ▒░
░  ░  ░  ░  ░░ ░  ░    ░ ░    ░ ░       ░ ░   ▒ ░  ░   ░ ░ ░ ░  ░   ░    ░░   ░ 
      ░  ░  ░  ░  ░  ░   ░  ░   ░  ░          ░          ░   ░      ░  ░  ░     
                                                           ░                    
"""


for col in banner:
    print(colors.CRED2 + col, end="")
    sys.stdout.flush()
    time.sleep(0.0025)

x = """
                Author:  3nCrypt | Xploit3R | Shell Finder
                Github:  https://github.com/X-3nCrypt
                   "take a coffee and keep hacking"
"""
for col in x:
    print(colors.CBLUE2 + col, end="")
    sys.stdout.flush()
    time.sleep(0.0040)

y = "\n\t\tHi there, Shall we play a game..? 😃\n"
for col in y:
    print(colors.CRED2 + col, end="")
    sys.stdout.flush()
    time.sleep(0.0040)

z = "\n"
for col in z:
    print(colors.ENDC + col, end="")
    sys.stdout.flush()
    time.sleep(0.4)


wordlist = [
    "shell.php",
    "admin/shell.php",
    "uploads/shell.php",
    "files/shell.php",
    "images/shell.php",
    "phpinfo.php",
    "config.php",
    "wp-config.php",
    "admin.php",
    "login.php",
    "upload.php"
]


def generate_paths(base_paths, length=3):
    chars = string.ascii_lowercase + string.digits + "_"
    for base in base_paths:
        yield base
        for combo in product(chars, repeat=length):
            yield f"{base}/{''.join(combo)}.php"
            yield f"{base}/{''.join(combo)}.php5"
            yield f"{base}/{''.join(combo)}.php7"


def heuristic_check(content):
    signatures = [
        "eval(", "base64_decode(", "shell_exec(", "exec(", "system(", "passthru(", "popen(", "proc_open("
    ]
    for signature in signatures:
        if signature in content:
            return True
    return False


def check_url(base_url, path):
    url = f"{base_url}/{path}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if heuristic_check(response.text):
                print(f"[{colors.CBLUE_DARK}{datetime.now().strftime('%H:%M:%S')}{colors.ENDC}] {colors.ENDC}[{colors.CGREEN_DARK}INFO{colors.ENDC}] File yang ditemukan: {url}")
                return url
        else:
            pass  # Do nothing for status code other than 200
    except requests.ConnectionError:
        pass  # Do nothing for connection errors
    except requests.Timeout:
        pass  # Do nothing for timeout errors
    except requests.RequestException:
        pass  # Do nothing for other request exceptions
    return None


def spinner_display(stop_event):
    spinner = ['.  ', '.. ', '...']
    spinner_index = 0
    while not stop_event.is_set():
        spinner_text = f"[{colors.CBLUE_DARK}{datetime.now().strftime('%H:%M:%S')}{colors.ENDC}] {colors.ENDC}[{colors.CGREEN_DARK}INFO{colors.ENDC}] {colors.CGREEN_LIGHT}Scanning{spinner[spinner_index]}{colors.ENDC}"
        print(spinner_text, end="\r")
        spinner_index = (spinner_index + 1) % len(spinner)
        time.sleep(0.5)


def scan_website(base_url, paths):
    found_files = []
    start_time = datetime.now()
    stop_spinner_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner_display, args=(stop_spinner_event,))
    spinner_thread.start()
    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(check_url, base_url, path): path for path in paths}
            for future in as_completed(future_to_url):
                result = future.result()
                if result:
                    found_files.append(result)
    except KeyboardInterrupt:
        print(f"{Fore.RED}\nScanning interrupted by user")
    finally:
        stop_spinner_event.set()
        spinner_thread.join()
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    return found_files, elapsed_time

if __name__ == "__main__":
    base_url = input(f"{colors.CGREEN2}Enter the URL (e.g. http://example.com): {colors.ENDC}").strip()
    if not base_url.startswith("http"):
        base_url = "http://" + base_url

    
    paths = list(generate_paths(wordlist, length=3))

    
    found_files, elapsed_time = scan_website(base_url, paths)

    
    print(f"\n{Fore.BLUE}[ Report Generation Phase Initiated. ]{Style.RESET_ALL}")
    print(f"Report of detected URLs for {base_url}")
    print(f"Total number of URLs detected by the webshell: {len(found_files)}")
    print(f"Total Time Elapsed for the Scan: {elapsed_time}")

    if found_files:
        print("\nFile yang ditemukan:")
        for file in found_files:
            print(file)
    else:
        print("\nTidak ada file yang ditemukan.")
