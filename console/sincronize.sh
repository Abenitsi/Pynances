#!/usr/bin/env bash

ls /Users/albert/Downloads | grep -e 'Movements.*' | xargs -I % mv -- /Users/albert/Downloads/% /Users/albert/Projects/Pynances/data/%
python main.py

rm -f ./data/*
