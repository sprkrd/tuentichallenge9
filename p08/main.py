#!/usr/bin/env python3

from os import makedirs
from os.path import splitext, join, dirname
from urllib.parse import urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup
from hashlib import md5


root = "http://52.49.91.111:8327/"
token = "?goodboy"
download_folder = "site"


def pageChildren(page):
    if splitext(page)[-1] not in ("", ".html", "htm"):
        return []
    children = []
    try:
        with urlopen(urljoin(root,page)+token) as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        links = soup("a")
        for link in links:
            try:
                children.append(urljoin(page,link["href"]))
            except KeyError:
                pass
    except Exception as e:
        print("Error occurred!: %s" % e)
    return children


def crawl():
    indexed_pages = set()
    stack = ["/"]
    while stack:
        top = stack.pop()
        if top in indexed_pages:
            continue
        indexed_pages.add(top)
        for child in pageChildren(top):
            if child != "../":
                stack.append(child)
    makedirs(download_folder, exist_ok=True)
    for page in indexed_pages:
        dst_file = join(download_folder, page[1:])
        if page.endswith("/"):
            dst_file = join(dst_file, "dirview.html")
        fullurl = urljoin(root,page)+token
        print("Downloading {} to {}...".format(fullurl, dst_file))
        try:
            with urlopen(fullurl) as web_stream:
                data = web_stream.read()
            makedirs(dirname(dst_file), exist_ok=True)
            with open(dst_file, "wb") as f:
                f.write(data)
        except Exception as e:
            print(fullurl + ": " + str(e))


def calculateAuthKey(user):
    nill_md5 = md5("nill".encode()).digest()
    user_md5 = md5(user.encode()).digest()
    auth_nill = bytes.fromhex("1c919b2d62b178f3c713bb5431c57cc1")
    # turns out that auth_key is 8e798f0377c99bc07cf1be129e35f8d5
    auth_user = [0]*16
    for i in range(16):
        auth_user[i] = ( auth_nill[i] - nill_md5[i] + user_md5[i] )%256
    return bytes(auth_user).hex()

if __name__ == "__main__":
    # crawl()
    print(calculateAuthKey("admin"))


