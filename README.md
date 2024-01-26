# EnOcean Hub

This project aims to act as an device hub which collects sensor data and puts it into InfluxDB Time-Series database and have for quick visualization with Grafana. 

![dashboard](https://yusufcanb.github.io/enohub/images/dashboard.png)

## Hardware Requirements

- EnOcean STM 550 Multisensor
- EnOcean USB 3000 Radio Receiver
- Raspberry Pi 3+

## Software Requirements

On Raspberry Pi you need to have below installed;

- Docker

## Quick Start

First, clone the project,

```
git clone https://github.com/yusufcanb/enohub
```

Then, create the config file with the sensor ids you have ,

```shell
cat << EOF > config.yaml
name: office
port: /dev/ttyUSB0

devices:
  - id: 04211ABE
    name: stm-550
    eep: d2-14-41
      
database:
  url: https://your-influxdb-host:port
  org: your-org
  token: your-access-token
  bucket: your-bucket
EOF
```

Finally, deploy it using Docker Compose,

```
docker compose up -d
```


Alternatively, if you already have InfluxDB on somewhere else and you just want pipe the data you may you the command below;  

```
docker run --rm --device=/dev/ttyUSB0 -v "$PWD/config.yaml:/opt/enocean/enohub/config.yaml" ghcr.io/yusufcanb/enohub:latest
```


## Docs

For more detailed documentation please navigate to the link below;
[https://yusufcanb.github.io/enohub/](https://yusufcanb.github.io/enohub/)