#!/bin/bash

PATH="~/anaconda3/bin:$PATH"
export PATH

pushd ~/Library/Scripts > /dev/null
python wzguest.py
popd > /dev/null

osascript -e 'display notification "Connected to the internet using wz guest" with title "Wifi Guest"'
