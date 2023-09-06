from python:3.9-slim-buster

run apt update && apt -y install \
        libopencv-dev

workdir /app

copy FastAPI/requirements.txt FastAPI/requirements.txt

run pip3 install -r FastAPI/requirements.txt

copy . .

env PORT 8000

cmd [ "/bin/sh", "-c", "./entrypoint.sh" ]
