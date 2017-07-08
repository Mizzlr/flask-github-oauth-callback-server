FROM python:3.5

MAINTAINER Mizzlr <mushtaque@codenation.co.in>

COPY requirements.txt /app/requirements.txt
RUN python3 -m pip install -r /app/requirements.txt

COPY server.py /app
COPY github.py /app
WORKDIR /app
RUN echo "[]" > data.json

CMD python3 server.py