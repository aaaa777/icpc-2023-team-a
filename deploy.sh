#!/bin/bash
#gcloud functions deploy icpc-a1 --region asia-northeast2 --entry-point entry_point --runtime python39 --trigger-http --allow-unauthenticated
#sudo docker build -t "icpc-a:latest" .
mv .gitignore .gitignore.bak
gcloud run deploy
mv .gitignore.bak .gitignore