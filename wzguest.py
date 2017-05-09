import requests

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

import urllib.parse
from urllib.request import Request, urlopen
from urllib.parse import urlparse

def getMagic(client, url) :
    print("+-[url] : {}".format(url))
    magic = None
    try :
        r = client.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        #print(soup)
        desc = soup.find("input", {"name":"magic"})
        magic = desc['value']
        print("+-[magic] : {}".format(magic))
    except :
        print("+-[magic] Cannot reach internet. Please wait")

    return magic

def letMeIn(client, baseurl, magic, username, password,redirurl) :
    # Send ok for CGU
    payload = urllib.parse.urlencode({
        '4Tredir':redirurl,
        'magic':magic,
        'answer':'1'
        })
    url = baseurl+"/fgtauth?"+magic
    print("+-[url] : {}".format(url))
    r = client.post(url, data=payload, headers=dict(Referer=url))
    #print("+-[status] : {} (need to be 200)".format(r.status))

    # Send credits
    payload = urllib.parse.urlencode({
        '4Tredir':redirurl,
        'magic':magic,
        'username':username,
        'password':password
        })
    url = baseurl+"/"
    print("+-[url] : {}".format(url))
    r = client.post(url, data=payload, headers=dict(Referer=url))
    #print("+-[status] : {} (need to be 303)".format(r.status))

if __name__ == "__main__":

    auth_tree = ET.parse("auth.xml")
    auth_root = auth_tree.getroot()

    for service in auth_root.findall('service') :
        if service.get("name") == "wzguest" :
            username = service.find("user").text
            password = service.find("password").text
            url = service.find("url").text
            redirurl = service.find("redirurl").text

    client = requests.session()
    magic = getMagic(client,redirurl)
    if magic :
        letMeIn(client,url,magic,username,password,redirurl)
