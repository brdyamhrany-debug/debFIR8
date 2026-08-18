import requests
import re
import os
from datetime import datetime

# ===================================================
#
# ===================================================

def fetch_proxies_from_sslproxies():
    """Fetch proxies from sslproxies.org"""
    try:
        url = "https://www.sslproxies.org/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        proxies = []
        pattern = r"<td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td>"
        matches = re.findall(pattern, resp.text)
        for ip, port in matches:
            proxies.append(f"{ip}:{port}")
        return proxies
    except Exception as e:
        print(f"\033[91m[!] Error fetching from sslproxies: {e}\033[0m")
        return []


def fetch_proxies_from_free_proxy_list():
    """Fetch proxies from free-proxy-list.net"""
    try:
        url = "https://free-proxy-list.net/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        proxies = []
        pattern = r"<td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td>"
        matches = re.findall(pattern, resp.text)
        for ip, port in matches:
            proxies.append(f"{ip}:{port}")
        return proxies
    except Exception as e:
        print(f"\033[91m[!] Error fetching from free-proxy-list: {e}\033[0m")
        return []


def test_proxy(proxy, timeout=5):
    """Test if a proxy is alive"""
    try:
        url = "http://httpbin.org/ip"
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        resp = requests.get(url, proxies=proxies, timeout=timeout)
        if resp.status_code == 200:
            return True
    except:
        pass
    return False


def save_proxies(proxies, filename="proxy_list.txt"):
    """Save proxies to a file"""
    try:
        download_path = os.path.join(
            os.path.expanduser("~"), "downloads", filename
        )
        save_dir = os.path.dirname(download_path)
        if not os.path.exists(save_dir):
            download_path = filename

        with open(download_path, "w", encoding="utf-8") as f:
            f.write(f"# Proxy List - Generated: {datetime.now()}\n")
            f.write(f"# Total: {len(proxies)}\n")
            f.write("# ============================================\n")
            for p in proxies:
                f.write(p + "\n")

        print(f"\033[91m[OK] {len(proxies)} proxies saved to {download_path}\033[0m")
        return download_path
    except Exception as e:
        print(f"\033[91m[!] Error saving file: {e}\033[0m")
        return None


def main():
    # Display ASCII Art at the start
    ascii_art = r"""
⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢻⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠰⣶⣶⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠙⢿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣼⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣼⣿⣿⠷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣟⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣿⣷⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣸⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⣤⡀⠀
⢺⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣷⡄
⠉⣿⣿⣿⣿⣿⣀⣀⣤⣴⣾⣿⣿⣿⣿⣿⠟⠁
⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀
⢐⠠⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠋⠀⠀⠀
⠈⢸⣿⣿⣿⣿⡿⢿⢏⠁⠀⠀⠀⠀⠀⠀⠀
⠃⢸⣿⣿⣿⣿⣇⠀⠄⠁⠀⠀⠀⠀⠀⠀
⡄⢸⣿⣿⣿⣿⣯⣥⡴⠀⠀⠀⠀⠀⠀⠀
⠀⢾⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀
⠀⠘⢿⣿⣿⣿⡿⠿⠿⢿⣿⣿⣿⡿⠀⠀
⠀⠀⢹⣿⣿⣏⠈⠀⠀⠀⠉⠙⠁⠀⠀
⠀⠀⠸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢰⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀
⡀⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⣸⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀
⠀⢾⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀
⠀⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀
⠀⢿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀
"""
    print(ascii_art)

    print("\033[91m             free proxy\033[0m")
    print("")

    print("\033[91m1 Fetching from sslproxies.org ...\033[0m")
    proxies1 = fetch_proxies_from_sslproxies()
    print(f"\033[91m   -> {len(proxies1)} proxies received.\033[0m")

    print("\033[91m2 Fetching from free-proxy-list.net ...\033[0m")
    proxies2 = fetch_proxies_from_free_proxy_list()
    print(f"\033[91m   -> {len(proxies2)} proxies received.\033[0m")

    # Merge and remove duplicates
    all_proxies = list(set(proxies1 + proxies2))
    print(f"\033[91m[OK] Total unique proxies: {len(all_proxies)}\033[0m")

    if len(all_proxies) == 0:
        print("\033[91m[!] No proxies received. Check your internet connection.\033[0m")
        return

    # Test proxies (optional - comment if you don't want this)
    print("\033[91m3 Testing proxies (may take a few seconds)...\033[0m")
    live_proxies = []
    for i, proxy in enumerate(all_proxies[:30], 1):
        print(f"\033[91m   Testing {i}/{min(30, len(all_proxies))}: {proxy}\033[0m", end=" ... ")
        if test_proxy(proxy):
            live_proxies.append(proxy)
            print("\033[91mOK\033[0m")
        else:
            print("\033[91mFAILED\033[0m")

    # If you don't want testing, use all_proxies instead
    if not live_proxies:
        print("\033[91m[!] No live proxies found (or testing skipped)\033[0m")
        final_proxies = all_proxies
    else:
        final_proxies = live_proxies

    # Save to file
    print("\033[91m4 Saving to file ...\033[0m")
    filepath = save_proxies(final_proxies)

    print("")
    if filepath:
        print(f"\033[91m   ...: {filepath}\033[0m")
        print("\033[91m   ......\033[0m")
    else:
        print("\033[91m   ❌ Error saving file.\033[0m")
    print("")


if __name__ == "__main__":
    main()
