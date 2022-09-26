import sys
from loguru import logger
from serial import SerialException

from pydantic import ValidationError
from .cli import EnOceanHubCLI

if __name__ == "__main__":
    try:
        cli = EnOceanHubCLI()
        cli.run()
    except SerialException as serial_exc:
        logger.error("Serial port communication failed")
        logger.error(serial_exc)
        sys.exit(-1)
    except ValidationError as validation_exc:
        logger.error("Config validation failed")
        logger.error(validation_exc)
        sys.exit(-1)
