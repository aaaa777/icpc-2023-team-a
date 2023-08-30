#!/bin/bash

sudo apt update
sudo apt install -y python3 python3-venv

sudo apt install -y ffmpeg build-essential

python3 -m venv venv

. venv/bin/activate

venv/bin/pip install -r requirements.txt