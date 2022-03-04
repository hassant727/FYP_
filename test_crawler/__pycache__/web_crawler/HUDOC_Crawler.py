from pathlib import Path

import requests
from bs4 import BeautifulSoup
from requests.models import Response

def crawl(base_url, start_anchor):
    search_anchors = queue.Queue()
    urls = []
    while True:
        if not start_anchor:
            start_anchor = '/'
        response = requests.request('GET', base_url + start_anchor)
        soup = BeautifulSoup(response.text, "lxml")
        anchors = find_local_anchors(soup, start_anchor)
        if anchors:
            for a in anchors:
                url = base_url + a
                if url in urls :
                    continue
                if not Path(a).suffix:
                    search_anchors.put(a)
                urls.append(url)
                print(url)
        
        if search_anchors.empty():
            break
        start_anchor = search_anchors.get()
    return urls        

def find_local_anchors(soup, start_anchor):
    anchors = []
    for link in soup.find_all('a'):
        anchor = link.attrs['href'] if 'href' in link.attrs else ''
        # print(anchor)
        if anchor.startswith(start_anchor):
            anchors.append(anchor)
    return anchors

url = "https://ocw.mit.edu"
start_anchor = "/"
urls = web_crawler.crawl(url, start_anchor)
print(len(urls))