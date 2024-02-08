from pydantic import BaseModel

from typing import List, Optional


class DatabaseConfig(BaseModel):
    url: str
    org: str
    token: str
    bucket: str

class Device(BaseModel):
    id: str
    name: str
    eep: str
    group: str

class EnoHubConfig(BaseModel):
    port: str
    devices: List[Device]
    database: DatabaseConfig
