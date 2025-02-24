from pydantic import BaseModel, Field

from typing import List, Optional


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    dbname: str
    schema_name: str = Field(default="public", alias="schema")


class Device(BaseModel):
    id: str
    name: str
    eep: str
    group: str


class EnoHubConfig(BaseModel):
    port: str
    devices: List[Device]
    database: DatabaseConfig
