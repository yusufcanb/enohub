import queue
from loguru import logger

from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.constants import PACKET
from enocean.protocol.packet import Packet

from .config import Device, EnoHubConfig
from .db import TimescaleDBClient


class EnOceanHub(SerialCommunicator):

    db: TimescaleDBClient
    config: EnoHubConfig

    def __init__(self, config: EnoHubConfig):
        super().__init__(config.port, callback=None)
        self.config = config
        self.db = TimescaleDBClient.from_enohub_config(config)

    def is_coming_from_registered_device(self, packet: Packet):
        for device in self.config.devices:
            if device.id.lower() == packet.sender_hex.replace(":", "").lower():
                return True
        return False

    def get_device_by_sender_hex(self, sender_hex: str) -> Device:
        for device in self.config.devices:
            if device.id.lower() == sender_hex.replace(":", "").lower():
                return device
        raise Exception("Device with given sender id not found")

    def parse_packet_by_config(self, packet: Packet):
        device = self.get_device_by_sender_hex(packet.sender_hex)
        _, func, typ = device.eep.split("-")
        packet.select_eep(int(func, base=16), int(typ, base=16))
        packet.parse_eep()
        logger.info(
            f"Packet parsed [sender_hex={packet.sender_hex}, eep={device.eep.lower()}]"
        )
        return packet

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

                if packet.packet_type != PACKET.RADIO_ERP1:
                    logger.info(
                        f"Only ERP1 packets are processed [sender_hex={packet.sender_hex}]"
                    )
                    continue

                packet = self.parse_packet_by_config(packet)
                for k in packet.parsed:
                    logger.debug("%s: %s" % (k, packet.parsed[k]))
                self.db.insert_packet(packet)
                logger.info(f"Packet inserted [sender_hex={packet.sender_hex}]")

            except queue.Empty:
                continue
            except KeyboardInterrupt:
                break
            except Exception as exc:
                logger.exception(exc)
