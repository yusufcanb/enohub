FROM python:3.8

LABEL org.opencontainers.image.source=https://github.com/yusufcanb/enohub
LABEL org.opencontainers.image.description="EnOcean Sensor Hub. Listens ESP3 packets from EnOcean USB 3000 usb stick and pipes into InfluxDB time-series database."

WORKDIR /opt/enocean/enohub

COPY . .

RUN apt-get install gcc

RUN pip install --upgrade pip
RUN pip3 install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["python3", "-W", "ignore", "-m", "enohub", "-c", "config.yaml"]