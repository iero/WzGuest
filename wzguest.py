# G. Fabre 05/2017 for Apple@Total project
# Updated 12/2017
#
# This script let you connect automaticaly to Total Guest network
#
# Install Dependencies :
# - pip install wireless
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
import requests

import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from wireless import Wireless

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getMagic(client, url) :
	print("+-[url] : {}".format(url))
	authstate = None
	hashst = None

	try :
		r = client.get(url, verify=False)
		# Test if already connected to internet
		if b'OK' in r.content :
			print("+-[Already Connected] !")
			return 0,0

		# Otherwise get url and hash number
		soup = BeautifulSoup(r.content, "html.parser")

		desc = soup.find("input", {"name":"AuthState"})
		authstate = desc['value']
		print("+-[authstate] : {}".format(authstate))

		desc = soup.find("input", {"name":"hash"})
		hashst = desc['value']
		print("+-[hash] : {}".format(hashst))

	except :
		print("+-[magic] Cannot reach internet. Please wait")

	return authstate, hashst

def letMeIn(client, baseurl, authstate, hashst, username, password, redirurl) :
	# Send credits
	try :
		payload = {
			'AuthState': authstate,
			'hash': hashst,
			'checkAup': 1,
			'username':username,
			'password':password,
			'accept_aup': 'on',
			'source': 'sponsor'
			}

		print("+-[url] : {}".format(baseurl))
		r = client.post(baseurl, data=payload, headers=dict(Referer=baseurl))

		# Force script to behave as a normal client (not needed if done using javascript browser)
		soup = BeautifulSoup(r.content, "html.parser")
		desc = soup.find("form", {"method":"post"})
		action_url = desc['action']
		print("+-[action url] : {}".format(action_url))

		desc = soup.find("input", {"name":"SAMLResponse"})
		saml = desc['value']
		print("+-[saml] : {}".format(saml))

		desc = soup.find("input", {"name":"RelayState"})
		relay = desc['value']
		print("+-[relay] : {}".format(relay))

		payload = {
			'SAMLResponse': saml,
			'RelayState': relay
			}

		r = client.post(action_url, data=payload, headers=dict(Referer=redirurl))

		# To test
		#print("+-[status] : {} (need to be 200)".format(r.status))

		if b'OK' in r.content :
			print("+-[Connected] to Internet !")
			return True
		else :
			return False
	except :
		return False

def checkNetwork(ssid) :
	timeout = 20
	sleeptime = 5
	loop = 0
	while loop < timeout :
		wireless = Wireless()
		s = wireless.current()

		# Connected to a wifi network
		if s is not None :
			# Total network
			if s == ssid :
				print("+-[Connected] to {}".format(ssid))
				return True
			# Another wifi network
			else :
				return True
		else :
			print("+-[Not connected] to {}. Waiting 5s to retry".format(ssid))
			time.sleep(sleeptime)
			loop +=1

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

	# Test if connected to the a wifi network
	if not checkNetwork(ssid) :
		sys.exit(1)

	# Catch captive portal and authentificate
	connected = False
	while not connected :
		client = requests.session()
		client.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
		authstate, hashst = getMagic(client,redirurl)

		if hashst == 0 :
			connected = True
			sys.exit(1)
		elif hashst :
			print('OK')
			connected = letMeIn(client,url,authstate,hashst,username,password,redirurl)

		if not connected :
			print("+-[Connection] failed. Wait 10s to retry")
			time.sleep(10)
