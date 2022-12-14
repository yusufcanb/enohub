FROM python:3.8

WORKDIR /opt/enocean/enohub

COPY . .

RUN apt-get install gcc

RUN pip install --upgrade pip
RUN pip3 install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["python3", "-W", "ignore", "-m", "enohub", "-c", "config.yaml"]