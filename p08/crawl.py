#!/usr/bin/env python3

from os import makedirs
from os.path import splitext, isdir, join
from urllib.parse import urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup

import tqdm
# from urlparse import urljoin


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
                children.append(link["href"])
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
    for page in tqdm.tqdm(indexed_pages):
        dst_file = join(download_folder, page)
        if page.endswith("/"):
            dst_file = join(dst_file, "dirview.html")
        fullurl = urljoin(root,page)+token
        try:
            with urlopen(fullurl) as web_stream:
                data = web_stream.read()
            with open(dst_file, "wb") as f:
                f.write(data)
        except Exception as e:
            print(fullurl + ": " + str(e))


print(crawl())


