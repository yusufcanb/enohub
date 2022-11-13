# Configuration

Enohub requires a custom declaration file in YAML format in order to configure its parameters. Here is an example configuration file to get started.

## Parameters

Available configuration parameters listed in dedicated sections;

### Root Object

| Parameter | Description                                                                                                           | Type   |
| --------- | --------------------------------------------------------------------------------------------------------------------- | ------ |
| name      | Display name of the sensor group. E.g living-room, kitchen, keller.                                                   | string |
| port      | Serial port which [EnOcean USB Stick](https://www.enocean.com/en/product/usb-300-500u-400j/?frequency=868) connected. | path   |
| devices   | Array of registered devices                                                                                           | array  |
| database  | Influx Time-Series database configuration                                                                             | object |


### Device Object

The parameters of the device listed below;

| Parameter | Description                                                                | Type   |
| --------- | -------------------------------------------------------------------------- | ------ |
| id        | Universal device identifier. Can be found on the backside of every device. | string |
| name      | A friendly name for the device.                                            | string |
| eep       | EEP of the device.                                                         | string |


### Database Object

The parameters of the InfluxDB configuration listed below;

| Parameter | Description                      | Type   |
| --------- | -------------------------------- | ------ |
| url       | # URL of the influxdb instance.  | string |
| org       | Organization name of the account | string |
| token     | Access Token for the client      | string |
| bucket    | Bucket name for the data points  | string |


## Example Configuration

```yaml
name: office
port: /dev/ttyUSB0

devices:
  - id: 04211ABE
    name: desk
    eep: d2-14-41
    
  - id: 04211945
    name: table
    eep: d2-14-41
  
  - id: 051B0025
    name: co2-meter
    eep: a5-09-09

database:
  url: https://your-influxdb-host:port
  org: your-org
  token: your-access-token
  bucket: your-bucket
```