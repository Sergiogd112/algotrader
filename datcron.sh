#!/bin/bash

if ! screen -list | grep -q "Datagraber"; then
  cd ~/
  screen -S Datagraber -d -m python3 ~/github/algotrader/Datagraber.py
fi

