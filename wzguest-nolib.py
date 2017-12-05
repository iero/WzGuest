# G. Fabre 05/2017 for Apple@Total project
# Updated 09/2017
#
# This script let you connect automaticaly to Total Guest network
#
# Install Dependencies :
# - Python 3 (using Anaconda for example)
#
# On Mac@Total macbooks, we use Apple session keychain to store connection credits
# - Launch install.bash and follow steps
#
# On Linux, no keychain available
# - Create auth.xml (example provided) with your creditential
# - Launch using 'wzguest.bash' or 'python wzguest.py auth.xml'
#
# If you change 'redirurl', make sure the target page contains 'OK' chain.

import time, sys

import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

# check python version
if sys.version_info >= (3,0):
    from urllib.parse import urlencode
else:
    from urllib import urlencode

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

def letMeIn(client, baseurl, magic, username, password, redirurl) :
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

    if len(sys.argv) < 2 :
        print(u"Please use # python wzguest.py auth.xml [opt user] [opt passwd]")
        sys.exit(1)

    if len(sys.argv) == 4 :
        username = sys.argv[2]
        password = sys.argv[3]

    auth_tree = ET.parse(sys.argv[1])
    auth_root = auth_tree.getroot()

    for service in auth_root.findall('service') :
        if service.get("name") == "wzguest" :
            if service.find('user') is not None :
                username = service.find("user").text
            if service.find('password') is not None :
                password = service.find("password").text
            url = service.find("url").text
            redirurl = service.find("redirurl").text
            ssid = service.find("ssid").text

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
