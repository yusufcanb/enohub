from typing import List, Optional

from enocean.protocol.packet import Packet
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, WriteApi

from enohub.config import EnoHubConfig


class CustomInfluxDBClient(InfluxDBClient):
    config: EnoHubConfig
    write_api: WriteApi

    def get_device_given_name(self, sender_hex: str):
        for device in self.config.devices:
            if device.id.lower() == sender_hex.replace(":", "").lower():
                return device.name
        return sender_hex.replace(":", "").lower()

    def get_device_config_by_sender_hex(self, sender_hex: str) -> Optional[dict]:
        for device in self.config.devices:
            if device.id.lower() == sender_hex.replace(":", "").lower():
                return device
        return None

    def insert_packet(self, packet: Packet):
        points: List[Point] = []
        for k in packet.parsed:
            if not k in ["TMP", "HUM", "ILL", "CO2", "ACC", "ACX", "ACY", "ACZ", "CO"]:
                continue
            p = Point(k)
            p.tag("sensor_group", self.config.name)
            p.tag("sensor_id", packet.sender_int)
            p.tag("sensor_name", self.get_device_given_name(packet.sender_hex))
            p.field("value", packet.parsed[k]["value"])
            points.append(p)
        self.write_api.write(bucket=self.config.database.bucket, record=points)

    @classmethod
    def from_enohub_config(cls, enohub_config: EnoHubConfig):
        client = CustomInfluxDBClient(
            url=enohub_config.database.url,
            token=enohub_config.database.token,
            org=enohub_config.database.org,
            timeout=30_000,
            retries=0,
        )
        client.config = enohub_config
        client.write_api = client.write_api(write_options=SYNCHRONOUS)
        return client
