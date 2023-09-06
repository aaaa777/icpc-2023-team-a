#!/bin/bash

sudo apt update
sudo apt install -y python3 python3-venv

# install ffmpeg
sudo apt install -y ffmpeg build-essential

# ask whether to install google cloud sdk
read -p "Install Google Cloud SDK? [y/N] " -n 1 -r

# install google cloud cli
sudo apt-get install apt-transport-https ca-certificates gnupg curl sudo
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-cli

# install docker
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# install apache2 and certbot
sudo apt install -y apache2 python3-certbot-apache

# configure apache2
sudo mkdir -p /var/www/icpc-a.nomiss.net
sudo chown -R www-data:www-data /var/www/icpc-a.nomiss.net
sudo a2enmod proxy
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

venv/bin/pip install -r requirements.txt