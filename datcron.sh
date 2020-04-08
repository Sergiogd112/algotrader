#!/bin/bash

if ! screen -list | grep -q "Datagraber"; then
  cd /home/pi/
  screen -S Datagraber -d -m python3 /home/pi/github/algotrader/Datagraber.py
fi

