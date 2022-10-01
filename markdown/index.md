# Overview

This project aims to act as an device hub which collects sensor data and puts it into InfluxDB Time-Series database for quick visualization. 


## Hardware Requirements

- EnOcean STM 550 Multisensor
- EnOcean USB 3000 Radio Receiver
- Raspberry Pi 3+

## Software Requirements

On Raspberry Pi you need them to be installed;

- Docker
- Docker Compose

AdditionallyOn somewhere on Cloud or you infrastructure you need InfluxDB

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
