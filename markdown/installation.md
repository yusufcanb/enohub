# Installation

## Docker

> **Note for Windows users**
>
> Docker installation on Windows is not supported since Serial port binding to containers is not possible. Please follow development installation guide for Windows and specify COM ports in the [configuration](../configuration) file.
> 

Before we begin, you need to have a configuration file. If you don't know how to create configuration files please navigate back to [Configuration](../configuration) section.

```
docker run --device=/dev/ttyUSB0 -v "$PWD/config.yaml:/opt/enocean/enohub/config.yaml" ghcr.io/yusufcanb/enohub:latest
```

The `--device` flag indicates the serial port which [EnOcean USB 3000](https://www.enocean.com/en/product/usb-300-500u-400j/?frequency=868) is connected to. This docker argument allows you to run devices inside the container without the `--privileged` flag.

## Development

For development purposes, you can use the instructions below in order the get start development.


First clone the repository,

```
git clone https://github.com/yusufcanb/enohub.git
```

Also pull submodules which is required for transcoding,

```
git submodule update --init
```

Then, using poetry install the dependencies,

```shell
pip3 install poetry  # Skip this if you already have poetry
poetry install --no-dev
```

Activate the environment using,

```
poetry shell
```