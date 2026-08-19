import time
import random
import sys
from colorama import Fore, Style, init

init(autoreset=True)


def print_slow(text, color=Fore.WHITE, speed=0.03):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(speed)
    print(Style.RESET_ALL)


def banner():
    banner_text = r"""
       _      wWw   ___      oo_
  /||_    (O)_ (___)__  /  _)-<
   /o_)   / __)(O)(O)   \__ `.
  / |(\  / (   /  _\       `. |
  | | ))(  _)  | |_))      _| |
  | |//  \ \_  | |_))_  ,-'   |
  \__/    \__) (.'-'(_)(_..--'
    """
    print(Fore.RED + "=" * 50)
    print_slow(banner_text, Fore.RED, 0.01)
    print(Fore.RED + "=" * 50 + "\n")


def simulate_brute_force():
    banner()

    username = input(Fore.WHITE + "[?] Enter Target Username: ")
    wordlist_path = input(Fore.WHITE + "[?] Enter Wordlist Path: ")

    print(f"\n{Fore.RED}[+] Initializing attack on: {username}...")
    time.sleep(1)
    print(f"{Fore.RED}[+] Loading payload list...")
    time.sleep(2)

    try:
        with open(wordlist_path, 'r') as file:
            passwords = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"\n{Fore.RED}[!] FATAL ERROR: Wordlist file not found!")
        return

    print(f"{Fore.RED}[+] Found {len(passwords)} potential candidates. Starting...\n")
    time.sleep(1)

    for i, pwd in enumerate(passwords):
        sys.stdout.write(f"\r{Fore.RED}[*] Attempting: {pwd} ({i+1}/{len(passwords)})")
        sys.stdout.flush()

        time.sleep(0.05)  

        
        if random.randint(1, 1000) == 7:
            print(f"\n\n{Fore.GREEN}{'='*40}")
            print_slow("  [!!!] ACCESS GRANTED [!!!]", Fore.GREEN, 0.1)
            print(f"{Fore.GREEN}  TARGET: {username}")
            print(f"{Fore.GREEN}  PASSWORD: {pwd}")
            print(f"{Fore.GREEN}{'='*40}")
            return

    print(f"\n\n{Fore.RED}[-] Attack Failed: Wordlist exhausted.")


if __name__ == "__main__":
    try:
        simulate_brute_force()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Process terminated by user.")
