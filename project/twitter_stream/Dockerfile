FROM python:3.6.5-slim

# install netcat
RUN apt-get update \
  && apt-get clean

# set working directory
RUN mkdir -p /usr/local/share/
WORKDIR /usr/local/share/

# add requirements
COPY ./requirements.txt /usr/local/share/requirements.txt

# install requirements
RUN pip install -r requirements.txt


COPY ./stream_listener.py /usr/local/share/stream_listener.py
CMD ["python", "./stream_listener.py"]