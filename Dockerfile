# git clone https://github.com/AmateurPirate/giwps.git

FROM python:3.7

WORKDIR /usr/src

RUN mkdir -p /usr/src/data

COPY requirements.txt /usr/src
COPY giwps.py /usr/src

RUN pip install --no-cache-dir -r requirements.txt