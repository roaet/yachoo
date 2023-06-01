import datetime
import json
import sys
import time
import urllib.parse

from bs4 import BeautifulSoup
import curlify
import requests

FIRST_GET = "https://www.yahoo.com"
SECOND_GET = "https://login.yahoo.com/account/create?.lang=en-US&src=homepage&activity=ybar-signin&pspid=2023538075&.done=https%3A%2F%2Fwww.yahoo.com%2F&specId=yidregsimplified&done=https%3A%2F%2Fwww.yahoo.com%2F"
POST = "https://login.yahoo.com/account/module/create?validateField=userId"
ERROR_URI = "https://login.yahoo.com/account/create/error"

def main():
    print("GET REQUESTS:")
    cookies = {}
    fp_data = ""
    with open("browserdata2", "r") as file:
        fp_data = file.read().strip()
    fp_json = json.loads(fp_data)
    dt = datetime.datetime.now()
    ms = dt.timestamp()*1000.0
    fp_json['ts'] = {
        "serve": int(ms),
        "render": int(ms) + 1201,
    }
    fp_data = json.dumps(fp_json)

    spec_data = ""
    with open("specdata", "r") as file:
        spec_data = file.read().strip()

    r = requests.get(SECOND_GET)
    header_keys = []
    cookie_keys = []
    for k, v in r.headers.items():
        header_keys.append(k)
    for k, v in r.cookies.items():
        cookie_keys.append(k)
    print(f"Headers: {header_keys}")
    print(f"Cookies: {cookie_keys}")
    cookies = r.cookies
    soup = BeautifulSoup(r.text, "html.parser")
    inputs = soup.find_all('input')
    data = {}
    for element in inputs:
        data[element.get('name')] = element.get('value')
    data["userId"] = "zach"

    cookie_elements = []
    for k, v in cookies.items():
        cookie_elements.append(f"{k}={v}")
    cookie_str = "; ".join(cookie_elements)

    print("POST REQUESTS:")
    data = urllib.parse.urlencode(data)

    headers = {
        'authority': 'login.yahoo.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie_str,
        'origin': 'https://login.yahoo.com',
        'referer': 'https://login.yahoo.com/account/create?.lang=en-US&src=homepage&activity=ybar-signin&pspid=2023538075&.done=https%3A%2F%2Fwww.yahoo.com%2F&specId=yidregsimplified&done=https%3A%2F%2Fwww.yahoo.com%2F',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    r = requests.request(
        "POST", POST, headers=headers, data=data, cookies=cookies
    )
    curl = curlify.to_curl(r.request)
    with open("curlcmd", "w") as outfile:
        outfile.write(curl)
    if r.url != POST:
        print("Redirected: probably an error")
    if r.url == ERROR_URI:
        print("Definitely an error. Cancelling")
        sys.exit(1)
    print(r.status_code)
    print(r.text)
    print(r.url)


if __name__ == "__main__":
    main()
