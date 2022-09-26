from pydantic import BaseModel
from typing import List, Type


class DeviceConfig(BaseModel):
    id: str
    eep: str


class DatabaseConfig(BaseModel):
    url: str
    org: str
    token: str
    bucket: str


class EnoHubConfig(BaseModel):
    name: str
    port: str
    devices: List[DeviceConfig]
    database: DatabaseConfig
