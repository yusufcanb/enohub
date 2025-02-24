import time
from typing import List, Optional
import psycopg2
from psycopg2.extras import execute_values

from enocean.protocol.packet import Packet
from loguru import logger

from enohub.config import EnoHubConfig


class TimescaleDBClient:
    def __init__(self, config: EnoHubConfig):
        self.config = config
        self.conn = None
        self.connect()

    def connect(self):
        """Connect to the TimescaleDB database."""
        try:
            self.conn = psycopg2.connect(
                host=self.config.database.host,
                port=self.config.database.port,
                user=self.config.database.user,
                password=self.config.database.password,
                dbname=self.config.database.dbname,
            )
            logger.info("Connected to TimescaleDB")
        except Exception as e:
            logger.error(f"Error connecting to TimescaleDB: {e}")
            raise

    def get_device_group(self, sender_hex: str) -> str:
        device_config = self.get_device_config_by_sender_hex(sender_hex)
        if device_config and device_config.group:
            return device_config.group
        return "default"

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
        """Insert sensor data into TimescaleDB."""
        if not self.conn or self.conn.closed:
            self.connect()

        cursor = self.conn.cursor()
        current_time_ms = int(time.time() * 1000)  # Current time in milliseconds

        # For latest data (ts_kv_latest)
        latest_data = []
        # For historical data (ts_kv)
        historical_data = []

        # Use sender_hex as device_id (without colons)
        device_id = packet.sender_hex.replace(":", "").lower()
        device_name = self.get_device_given_name(packet.sender_hex)
        device_group = self.get_device_group(packet.sender_hex)

        try:
            for k in packet.parsed:
                if not k in [
                    "TMP",
                    "HUM",
                    "ILL",
                    "CO2",
                    "ACC",
                    "ACX",
                    "ACY",
                    "ACZ",
                    "CO",
                ]:
                    continue

                key = k.lower()  # Use lowercase for keys
                value = packet.parsed[k]["value"]

                # Determine which value column to use based on the data type
                bool_v = None
                str_v = None
                long_v = None
                dbl_v = None
                json_v = None

                if isinstance(value, bool):
                    bool_v = value
                elif isinstance(value, str):
                    str_v = value
                elif isinstance(value, int):
                    long_v = value
                elif isinstance(value, float):
                    dbl_v = value
                else:
                    # Convert any other types to string
                    str_v = str(value)

                # Add to latest data
                latest_data.append(
                    (
                        device_id,
                        device_name,
                        device_group,
                        key,
                        current_time_ms,
                        bool_v,
                        str_v,
                        long_v,
                        dbl_v,
                        json_v,
                    )
                )

                # Add to historical data
                historical_data.append(
                    (
                        device_id,
                        device_name,
                        device_group,
                        key,
                        current_time_ms,
                        bool_v,
                        str_v,
                        long_v,
                        dbl_v,
                        json_v,
                    )
                )

            # Insert into ts_kv_latest table (with UPSERT)
            if latest_data:
                query = """
                INSERT INTO {}.ts_kv_latest 
                    (device_id, device_name, device_group, key, ts, bool_v, str_v, long_v, dbl_v, json_v) 
                VALUES %s 
                ON CONFLICT (device_id, key) 
                DO UPDATE SET 
                    device_name = EXCLUDED.device_name,
                    device_group = EXCLUDED.device_group,
                    ts = EXCLUDED.ts,
                    bool_v = EXCLUDED.bool_v,
                    str_v = EXCLUDED.str_v,
                    long_v = EXCLUDED.long_v,
                    dbl_v = EXCLUDED.dbl_v,
                    json_v = EXCLUDED.json_v
                """.format(
                    self.config.database.schema_name
                )

                execute_values(cursor, query, latest_data)

            # Insert into ts_kv table (historical data)
            if historical_data:
                query = """
                INSERT INTO {}.ts_kv 
                    (device_id, device_name, device_group, key, ts, bool_v, str_v, long_v, dbl_v, json_v) 
                VALUES %s
                """.format(
                    self.config.database.schema_name
                )

                execute_values(cursor, query, historical_data)

            self.conn.commit()
            logger.debug(f"Inserted {len(latest_data)} records into TimescaleDB")

        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error inserting data into TimescaleDB: {e}")
            raise
        finally:
            cursor.close()

    @classmethod
    def from_enohub_config(cls, enohub_config: EnoHubConfig):
        return cls(enohub_config)
