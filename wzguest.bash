#!/bin/bash

# For Mac@Total users only
PATH="/Users/$USER/anaconda/bin:/Users/$USER/anaconda3/bin:$PATH"
export PATH

APPL="/Users/$USER/Library/Application Scripts/com.total.network"

#PYTHON_VERSION=`python -c 'import sys; version=sys.version_info[:3]; print("{0}".format(*version))'`

/usr/bin/security find-generic-password -s WzGuest >/dev/null 2>&1
if [ $? -eq 0 ]; then
  user=$(/usr/bin/security find-generic-password -s WzGuest | grep acct | awk -F '\"' '{print $4}')
  pwd=$(/usr/bin/security find-generic-password -s WzGuest -w)

  python "$APPL/wzguest.py" "$APPL/auth.xml" $user $pwd
  if [ $? -eq 0 ]; then
    osascript -e 'display notification "Connected to the internet using wz guest" with title "Wifi Guest"'
  fi
fi
