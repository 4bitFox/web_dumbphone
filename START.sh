#!/bin/sh

waydroid session start &
ydotoold &

cd /var/mnt/data/web_dumbphone/
./python/bin/python3 main.py
