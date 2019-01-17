FROM python:3.6.5-slim

# install netcat
RUN apt-get update \
  && apt-get clean

# set working directory
RUN mkdir -p /usr/src/app/twitter_stream
WORKDIR /usr/src/app/twitter_stream

# add requirements
COPY ./requirements.txt /usr/src/app/twitter_stream/requirements.txt

# install requirements
RUN pip install -r requirements.txt


COPY ./stream_listener.py /usr/src/app/twitter_stream/stream_listener.py
RUN python stream_listener.py