FROM python:3.11-buster as builder

WORKDIR /opt/enocean/enohub
RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

COPY . .
RUN poetry install --without dev --no-root

FROM python:3.11-slim-buster as runtime

LABEL org.opencontainers.image.source=https://github.com/yusufcanb/enohub
LABEL org.opencontainers.image.description="EnOcean Sensor Hub. Listens ESP3 packets from EnOcean USB 3000 usb stick and pipes into InfluxDB time-series database."

WORKDIR /opt/enocean/enohub

ENV PATH="/opt/enocean/enohub/.venv/bin:$PATH"

COPY --from=builder /opt/enocean/enohub /opt/enocean/enohub

CMD ["python3", "-W", "ignore", "-m", "enohub", "-c", "config.yml"]
