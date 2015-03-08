#!/usr/bin/python
# -*- coding: utf-8 -*-
import http.client, os, sys
from urllib.parse import urlparse

utf8stdout = open(1, 'w', encoding='utf-8', closefd=False) # fd 1 is stdout

def urlretrieve(url, path):
    url = urlparse(url)
    conn = http.client.HTTPConnection(url.hostname)
    conn.request("GET", url.path)
    r = conn.getresponse()
    output = open(path.encode('utf-8'),'wb')
    output.write(r.read())
    output.close()

def downImgur(name, downDir = 'manga-down/'):
    if not os.path.isdir(downDir) :
        os.mkdir(downDir)
    print('{0}::download start!'.format(name))

    conn = http.client.HTTPConnection(name+".imgur.com")
    conn.request("GET", "")
    r = conn.getresponse()
    source = r.read()
    source = source.decode("utf-8")
    max = source.count('<div id="album-')
    cnt = 0
    while source.find('<div id="album-') != -1 :
        cnt += 1
        source = source[source.find('<div id="album-')+len('<div id="album-'):]
        item_url = source[0:source.find('"')]
        source = source[source.find('data-title="')+len('data-title="'):]
        item_title = source[0:source.find('"')]
        item_title = item_title.replace('/', '-').replace('\\', '-').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('\'', '').replace('<', '').replace('>', '').replace('|', '')
        if not os.path.isdir(downDir.encode('utf-8')+item_title.encode('utf-8')) :
            os.mkdir(downDir+item_title)
            print("[{0}/{1}][{3:3.0f}%]'{2}' Downloading...".format(cnt, max,
                item_title, 0), end="\r", flush=True, file=utf8stdout)

        conn = http.client.HTTPConnection("imgur.com")
        conn.request("GET", "/a/"+item_url)
        item_res = conn.getresponse()
        item_source = item_res.read()
        item_source = item_source.decode("utf-8")
        item_max = item_source.count('<a href="/download/')
        i = 0
        while item_source.find('<a href="/download/') != -1 :
            item_source = item_source[item_source.find('<a href="/download/')+len('<a href="/download/'):]
            imgname = item_source[0:item_source.find('"')]
            urlretrieve("http://i.imgur.com/"+imgname+".jpg",
                u"{0}{1}/{2}.jpg".format(downDir, item_title, i))
            i += 1
            print("[{0}/{1}][{3:3.0f}%]'{2}' Downloading...".format(cnt, max, item_title,
                i/item_max * 100), end="\r", flush=True, file=utf8stdout)
        print("")
    print('{0}::done!'.format(name))

if __name__ == '__main__':
    for subname in sys.argv[1:]:
        downImgur(subname)
