# G. Fabre 05/2017 for Apple@Total project
#
# This script is able to connect automaticaly to Total Guest network
#
# Install :
# Create auth.xml (example provided) with your creditential
# Launch using wzguest.bash or python wzguest.py
#
# Dependencies :
# - Python 3
# - pip install wireless

import requests
import time
import sys

from wireless import Wireless

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
        # Test if already connected to internet
        if b'OK' in r.content :
            print("+-[Already Connected] !")
            return 0

        # Otherwise get magic number
        soup = BeautifulSoup(r.content, "html.parser")
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
    if b'OK' in r.content :
        print("+-[Connected] to Internet !")
        return True
    else :
        return False

if __name__ == "__main__":

    auth_tree = ET.parse("auth.xml")
    auth_root = auth_tree.getroot()

    for service in auth_root.findall('service') :
        if service.get("name") == "wzguest" :
            username = service.find("user").text
            password = service.find("password").text
            url = service.find("url").text
            redirurl = service.find("redirurl").text
            ssid = service.find("ssid").text

    # Test if connected to the right wifi network
    connected = False
    while not connected :
        wireless = Wireless()
        s = wireless.current()
        if s == ssid :
            print("+-[Connected] to {}".format(ssid))
            connected = True
        else :
            print("+-[Not connected] to {}. Wait 5s to retry".format(ssid))
            time.sleep(5)

    # Catch captive portal and authentificate
    connected = False
    while not connected :
        client = requests.session()
        magic = getMagic(client,redirurl)

        if magic == 0 :
            connected = True
            sys.exit(0)
        elif magic :
            connected = letMeIn(client,url,magic,username,password,redirurl)

        if not connected :
            print("+-[Connection] failed. Wait 10s to retry")
            time.sleep(10)
