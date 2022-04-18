# write your code here
import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore

files = []
save_dir = sys.argv[1]
stack = deque()
url_prev = ""

if not os.path.exists(save_dir):
    os.mkdir(save_dir)

while True:
    url = input()
    if url == "exit":
        break
    if url == "back":
        try:
            back_url = stack.pop()
        except IndexError:
            continue
        url = back_url
    else:
        if url_prev:
            stack.append(url_prev)
    if url in files:
        file = open(f"{save_dir}\\{url}", "r", encoding="utf-8")
        print(file.read())
        file.close()
        prev_url = url
    else:
        if url[0: 9] != "https://":
            web_url = "https://" + url
        else:
            web_url = url
            url = url[9: -4]
        try:
            website = requests.get(web_url)
            if not website.status_code:
                print("Incorrect URL")
                continue
            website = BeautifulSoup(website.content, "html.parser")
            for elm in website.descendants:
                if elm.name == 'a':
                    print(Fore.BLUE + elm.text)
                    continue
                try:
                    print(elm.text)
                except AttributeError:
                    pass
            file = open(f"{save_dir}\\{url}", "w", encoding="utf-8")
            file.write(website.get_text())
            file.close()
            files.append(url)
            url_prev = url
        except requests.exceptions.ConnectionError:
            print("Incorrect URL")
