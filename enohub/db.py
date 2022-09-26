from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from enohub.config import EnoHubConfig

def get_database_client(enohub_config: EnoHubConfig):
    client = InfluxDBClient(url=enohub_config.database.host, token=enohub_config.database.port, org=enohub_config.database.credentials["org"], timeout=120, retries=0)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    read_api = client.query_api()
    return read_api, write_api
