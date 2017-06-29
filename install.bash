#!/bin/bash

cp wzguest.* ~/Library/Scripts/
cp auth.xml ~/Library/Scripts/

cp wifi.wzguest.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/wifi.wzguest.plist
