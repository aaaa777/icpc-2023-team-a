#!/bin/bash

sudo apt update
sudo apt install -y python3 python3-venv

# install ffmpeg
sudo apt install -y ffmpeg build-essential

# install apache2 and certbot
sudo apt install -y apache2 python3-certbot-apache

# configure apache2
sudo cp apache/010_apache.conf /etc/apache2/sites-available/010_icpc_a.conf
sudo a2ensite 010_icpc_a.conf

# create ssl certificate
sudo certbot --apache

# create fastapi service
sudo cp FastAPI/fastapi.service /etc/systemd/system/fastapi.service
sudo systemctl daemon-reload
sudo systemctl enable fastapi.service
sudo systemctl start fastapi.service

# install python packages
cd FastAPI
python3 -m venv venv

. venv/bin/activate

pip install -r requirements.txt