import queue
from loguru import logger

from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.constants import PACKET, RORG

from .config import EnoHubConfig


def loop(config: EnoHubConfig) -> None:
    logger.info("EnOncean USB 3000 Agent started")
    communicator = SerialCommunicator(port=config.port)
    communicator.start()
    logger.info("Communicator started")
    while communicator.is_alive():
        try:
            packet = communicator.receive.get(block=True, timeout=1)
            logger.info(f"Received new packet")
            if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.VLD:
                packet.select_eep(0x14, 0x41)
                packet.parse_eep()
            if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.BS4:
                # parse packet with given FUNC and TYPE
                for k in packet.parse_eep(0x02, 0x05):
                    logger.info("%s: %s" % (k, packet.parsed[k]))
            if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.BS1:
                # alternatively you can select FUNC and TYPE explicitely
                packet.select_eep(0x00, 0x01)
                # parse it
                packet.parse_eep()
                for k in packet.parsed:
                    logger.info("%s: %s" % (k, packet.parsed[k]))
            if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.RPS:
                for k in packet.parse_eep(0x02, 0x02):
                    logger.info("%s: %s" % (k, packet.parsed[k]))
        except queue.Empty:
            continue
        except KeyboardInterrupt:
            break
        except Exception as exc:
            logger.exception(exc)
