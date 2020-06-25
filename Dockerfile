FROM python:3.7

WORKDIR /usr/src

COPY requirements.txt /usr/src
COPY giwps.py /usr/src

RUN pip install --no-cache-dir -r requirements.txt

RUN python3 giwps.py -floor 1000 -ceiling 1200