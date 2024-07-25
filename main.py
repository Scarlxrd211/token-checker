# Github: https://github.com/Scarlxrd211
# Please dont be a skid...

import os
import time
import json
import requests
import sys
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)

Y = Fore.YELLOW
W = Fore.WHITE
G = Fore.GREEN
R = Fore.RED
C = Fore.CYAN
V = Fore.MAGENTA

valids = 0
invalids = 0
locked = 0
rate = 0
nitro_boost = 0
nitro_classic = 0

def gettime():
    return datetime.now().strftime("%H:%M:%S")

def clear():
    return os.system('cls')

def init_checker():
    ouput_files = ["invalids.txt", "valid.txt", "locked.txt"]
    clear()
    choice = input(f"{V}[?] Do you want clear old output files (yes/no)?: ")
    if choice.lower() == "yes":
        for filename in ouput_files:
            with open(f"data/{filename}", 'w') as f:
                pass
        print(f"{G}[+] All old input files are cleared. Lets check your tokens.")
        time.sleep(2)
        return True
    else:
        return True

def check_file_content(file_path):
    with open(file_path, 'r') as f:
        if len(f.read().splitlines()) == 0:
            clear()
            input(f"{Y}[!] Any Tokens Found in file '{file_path}' Press Enter To Continue...")
            return False
        else:
            with open(file_path, 'r') as f:
                token_list = []
                [token_list.append(token) for token in f.read().splitlines()]
                return token_list

def check_verify(content):
    ev = ""
    fv = ""
    mail = content.get('verified')
    phone = content.get('phone')
    if mail != False:
        ev += "YES"
    else:
        ev += "NO"
    if phone != False:
        fv += "YES"
    else:
        fv += "NO"
    return ev, fv
  
def get_req_code(token):
    global nitro_boost, nitro_classic
    headers = {"Authorization": token}
    req = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    if req.status_code == 200:
        response = req.json()
        ev, fv = check_verify(response)
        boost = False
        nitro_type = None
        if response.get('premium_type') == 1:
            nitro_type = "Nitro Basic"
            nitro_classic += 1
        elif response.get('premium_type') == 2:
            nitro_type = "Nitro Boost"
            nitro_boost += 1
            boost = check_boost(token)
        else:
            nitro_type = "No Nitro"
        return "valid", nitro_type, ev, fv, boost
    elif req.status_code == 403:
        return "locked", False, False, False, False
    elif req.status_code == 429:
        return "rate limited", False, False, False, False
    else:
        return "invalid", False, False, False, False

def check_boost(token):
    headers = {"Authorization": token}
    req = requests.get('https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots', headers=headers)
    return sum(1 for item in req.json() if item.get('premium_guild_subscription') is not None) 

def check_nitro_ending(token):
    headers = {"Authorization": token}
    req = requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers=headers)
    if req.status_code == 200:
        return 30 - datetime.fromisoformat(req.json()[0].get("current_period_end")).day 
        
def save_into_file(file_path, token):
    try:
        with open(file_path, 'a') as f:
            f.write(token + "\n")
        return True 
    except Exception as e:
        return False

def main():
    global valids, invalids, locked, rate, nitro_boost, nitro_classic
    init_checker()
    check = check_file_content("data/tokens.txt")
    if check == False:
        return sys.exit(1)
    clear()
    print(f'Output Format: {W}(Hour){G}[+] Token Checkd Token.. {W}[{V}Nitro Type{W}][{V}DAY LEFT{W}][{V}EV{W}][{V}FV{W}][{V}Active Boost{W}] Time Taken: in sec\n')
    for tokens in check:
        sys.stdout.write(f'\x1b]2;{valids} Valids / {locked} Locked / {invalids} Invalids\x07')

        token = tokens.strip()
        now = time.time()
        status, nitro_type, ev, fv, boost = get_req_code(token)
        if status == "valid":
            valids += 1
            save = save_into_file("data/valid.txt", token)
            if save == True:
                if nitro_type == "Nitro Boost":
                    ending = check_nitro_ending(token)
                    print(f'{W}({gettime()}){G}[+] Token {token[:24]}.**.*** {W}[{V}{nitro_type}{W}][{V}{ending} DAY LEFT{W}][{V}{ev}{W}][{V}{fv}{W}][{V}{boost} USED{W}] Time Taken: {time.time() - now:.2f} sec')
                elif nitro_type == "Nitro Basic":
                    print(f'{W}({gettime()}){G}[+] Token {token[:24]}.**.*** {W}[{V}{nitro_type}{W}][{V}{ending} DAY LEFT{W}][{V}{ev}{W}][{V}{fv}{W}] Time Taken: {time.time() - now:.2f} sec')
                else:
                    print(f'{W}({gettime()}){G}[+] Token {token[:24]}.**.*** {W}[{V}{nitro_type}{W}][{V}{ev}{W}][{V}{fv}{W}] Time Taken: {time.time() - now:.2f} sec')
            else:
                print(f'{W}({gettime()}){R}[x] Failed To Save Token In File.')
        elif status == "rate limited":
            rate += 1
            save = save_into_file('data/to_recheck.txt', token)
            if save == True:
                print(f'{W}({gettime()}){Y}[!] Token {token[:24]}.**.*** {W} You Are Behing Rate Limited. Sleeping for 4 Seconds...')
                time.sleep(4)
            else:
                print(f'{W}({gettime()}){R}[x] Failed To Save Token In File.')
            time.sleep(4)
        elif status == "locked":
            locked += 1
            save = save_into_file('data/locked.txt', token)
            if save == True:
                print(f'{W}({gettime()}){G}[+] Token {token[:24]}.**.*** {W}Time Taken {time.time() - now:.2f} sec')
            else:
                print(f'{W}({gettime()}){R}[x] Failed To Save Token In File.')
        elif status == "invalid":
            invalids += 1
            save = save_into_file('data/invalids.txt', token)
            if save == True:
                print(f'{W}({gettime()}){R}[x] Token {token[:24]}.**.*** {W}Time Taken {time.time() - now:.2f} sec')
            else:
                print(f'{W}({gettime()}){R}[x] Failed To Save Token In File.')
    input(f"{G}[@] Checker Results: {W}{valids} {G}Valids / {W}{invalids}{G} Invalids / {W}{locked} {G}Locked / {W}{rate} {G}Rate Limited / {W}{nitro_boost} {G}Nitro Boost / {W}{nitro_classic} {G}Nitro Classic")


if __name__ == "__main__":
    main()