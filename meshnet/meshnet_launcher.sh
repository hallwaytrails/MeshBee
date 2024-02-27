#!/bin/bash

# Abort startup if another instance was found    
pgrep -f '/opt/meshnet/venv/bin/python gui.py' > /dev/null && {
  exit
}

/opt/meshnet/venv/bin/python /opt/meshnet/gui.py

