FROM python:3.8

RUN apt-get install gcc

RUN pip install --upgrade pip
RUN pip3 install poetry

WORKDIR /influxdb
RUN wget https://dl.influxdata.com/influxdb/releases/influxdb2-client-2.7.3-linux-amd64.tar.gz
RUN tar xvzf ./influxdb2-client-2.7.3-linux-amd64.tar.gz
RUN cp ./influx /usr/local/bin/


WORKDIR /workspace

# RUN poetry config virtualenvs.create false
# RUN poetry install --no-dev
