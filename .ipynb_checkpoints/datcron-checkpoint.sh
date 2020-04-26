#!/bin/bash

if ! screen -list | grep -q "Datagraber"; then
  cd /home/sergio/
  screen -S Datagraber -d -m python3 /home/sergio/github/algotrader/Datagraber.py
fi

