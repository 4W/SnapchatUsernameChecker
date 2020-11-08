import requests
import os
import uuid
import time
import random
import concurrent.futures
import time
import json

proxylist = open('proxies.txt').read().splitlines()
userlist = open('usernames.txt').read().splitlines()

def getWebID():
    id = uuid.uuid4()
    id = str(id)
    return id




def sendWebhook(name):

    url = "YOUR WEBHOOK"

    data = {}

    data["content"] = "@everyone"
    data["username"] = "bruh checka"


    data["embeds"] = []
    embed = {}


    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    embed["description"] = f"Username was found at {current_time}"
    embed["title"] = f"{name} is available"
    data["embeds"].append(embed)

    requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})

def getXsrfToken():
    headers = {
        'authority': 'accounts.snapchat.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    r = requests.get("https://accounts.snapchat.com/accounts/signup?client_id=scan", headers=headers)
    data = r.text
    data = str(data)
    xsrf = data.split('data-xsrf="')[1]
    xsrf = xsrf.split('"')[0]
    return xsrf

def checkUser(username):
    proxy = random.choice(proxylist)
    proxy = {'https':'https://' + proxy}
    xsrf = getXsrfToken
    id = getWebID()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.5",
        "referer": "https://accounts.snapchat.com/",
        "cookie": f"xsrf_token={xsrf}; sc-cookies-accepted=true; web_client_id={id}; oauth_client_id=c2Nhbg==",
        "connection": "keep-alive",
        "content-type": "application/x-www-form-urlencoded; charset=utf-8",
        }

    finalURL = f"https://accounts.snapchat.com/accounts/get_username_suggestions?requested_username={username}&xsrf_token={xsrf}"



    r = requests.post(finalURL, headers=headers, proxies=proxy)
    content = r.text
    statuscode = r.status_code
    if statuscode == 429:
        print("RATELIMITED")
        return None
    else:
        if "TAKEN" in content:
            print(f"[*] {username}")
        elif "OK" in content:
            print(f"[AVAILABLE]{username}")
            f = open("available.txt", "a+")
            f.write(f"{username}\n")
            f.close()
            sendWebhook(username)
        elif "DELETED" in content:
            print(f"[DELETED / BANNED] {username}")
        else:
            print("==================================")
            print("WTF UNKNOWN ERROR")
            print(r.text)
            print("==================================")

    


def initialize():
    os.system("cls")
    print("==========================")
    print("")
    print("4W#2100 | Snapchat Checker")
    print("")
    print("")
    print("==========================")
    print("")
    print("Threads:")
    thread_count = input("> ")
    thread_count = int(thread_count)
    print("")
    input("Press 'ENTER' to start")
    count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        for username in userlist:
            executor.submit(checkUser, username)

    print(f"DONE WITH ALL")






initialize()
