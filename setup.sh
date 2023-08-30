#!/bin/bash

sudo apt update
sudo apt install -y python3 python-venv

sudo apt install -y ffmpeg build-essential

python3 -m venv venv

. venv/bin/activate

pip install -r requirements.txt