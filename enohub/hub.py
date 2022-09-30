import queue
from loguru import logger


from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.constants import PACKET, RORG
from enocean.protocol.packet import Packet

from .config import EnoHubConfig
from .db import CustomInfluxDBClient


class EnOceanHub(SerialCommunicator):

    db: CustomInfluxDBClient
    config: EnoHubConfig

    def __init__(self, config: EnoHubConfig):
        super().__init__(config.port, callback=None)
        self.config = config
        self.db = CustomInfluxDBClient.from_enohub_config(config)

    def is_coming_from_registered_device(self, packet: Packet):
        for device_dict in self.config.devices:
            if device_dict["id"].lower() == packet.sender_hex.replace(":", "").lower():
                return True
        return False

    def loop(self):
        self.start()
        logger.info("EnOcean Hub started")
        while self.is_alive():
            try:
                packet = self.receive.get(block=True, timeout=1)
                logger.info(f"Received new packet [sender_hex={packet.sender_hex}]")
                if not self.is_coming_from_registered_device(packet):
                    logger.info(f"Packet dropped [sender_hex={packet.sender_hex}]")
                    continue
                if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.VLD:
                    packet.select_eep(0x14, 0x41)
                    packet.parse_eep()
                    for k in packet.parsed:
                        logger.debug("%s: %s" % (k, packet.parsed[k]))
                    self.db.insert_packet(packet)
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
