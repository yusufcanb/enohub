from pydantic import BaseModel
from typing import List


class DatabaseConfig(BaseModel):
    url: str
    org: str
    token: str
    bucket: str

class Device(BaseModel):
    id: str
    name: str
    eep: str

class EnoHubConfig(BaseModel):
    name: str
    port: str
    devices: List[Device]
    database: DatabaseConfig
