#!/bin/bash

PATH="~/anaconda3/bin:$PATH"
export PATH

pushd ~/WzGuest > /dev/null
python wzguest.py
popd > /dev/null
