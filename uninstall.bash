#!/bin/bash

APPL="/Users/$USER/Library/Application Scripts/com.total.network"
SCPT="/Users/$USER/Library/Scripts/"

# Unload and remove deamon
launchctl unload com.total.wzguest
rm /Users/$USER/Library/LaunchAgents/com.total.wzguest.plist

# Remove Application files
rm "$APPL/wzguest.*"
rm "$APPL/auth.xml"

# Remove Application directory if empty
if find "$APPL" -mindepth 1 -print -quit | grep -q .; then
	echo "$APPL not empty.. keeping"
else
	echo "$APPL empty.. removing"
	rm -rf "$APPL"
fi

# Remove Wifi password in keychain
/usr/bin/security find-generic-password -s WzGuest >/dev/null 2>&1
if [ $? -eq 0 ]; then
	/usr/bin/security delete-generic-password -s WzGuest
	echo "Delete WzGuest entry in keychain"
fi

# Restore Captive portal
echo "Please enter your (user) password to reactivate captive portal : "
sudo defaults delete /Library/Preferences/SystemConfiguration/com.apple.captive.control Active
