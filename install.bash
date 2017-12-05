#!/bin/bash

# Desactivate Captive portal
defaults read /Library/Preferences/SystemConfiguration/com.apple.captive.control.plist >/dev/null 2>&1
if [[ $? != 0 ]]; then
	echo "Please enter your (user) password to desactivate captive portal : "
	sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.captive.control Active -boolean false
fi

# if needed, reactivate using :
# sudo defaults delete /Library/Preferences/SystemConfiguration/com.apple.captive.control Active

# Save wifi credits to keychain
/usr/bin/security find-generic-password -s WzGuest >/dev/null 2>&1
if [ $? -eq 0 ]; then
	echo "WzGuest entry alredy found in keychain"
else
	echo "WzGuest entry not found in keychain"
	read -p "Enter your Total email (firstname.lastname@total.com) : " email
	read -p "Enter your Wifi Guest password : " pwd
	/usr/bin/security add-generic-password -s WzGuest -a $email -w $pwd
fi

APPL="/Users/$USER/Library/Application Scripts/com.total.network"
SCPT="/Users/$USER/Library/Scripts"

if [ ! -d "$APPL" ] ; then mkdir -pv "$APPL" ; fi
if [ ! -d "$SCPT" ] ; then mkdir -pv "$SCPT" ; fi

cp mac_auth.xml "$APPL/auth.xml"
cp wzguest.py "$APPL/"
cp wzguest.bash "$APPL/"

if [ ! -f $SCPT/wzguest.bash ] ; then
	ln -s "$APPL/wzguest.bash" "$SCPT/"
fi

if [ "$(launchctl list | grep com.total.wzguest | wc -l)" -eq 1 ] ; then
	echo "Unload agent"
	launchctl unload /Users/$USER/Library/LaunchAgents/com.total.wzguest.plist
fi

sed s/USERNAME/$USER/ com.total.wzguest.plist > /Users/$USER/Library/LaunchAgents/com.total.wzguest.plist
launchctl load /Users/$USER/Library/LaunchAgents/com.total.wzguest.plist
echo "Load agent"
