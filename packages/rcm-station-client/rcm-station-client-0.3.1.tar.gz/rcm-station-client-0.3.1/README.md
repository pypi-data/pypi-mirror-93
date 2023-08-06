# Station client

Scripts to read one or multiple sensors connected to the I2C bus on a Raspberry Pi and submit them to the station-monitoring-service.

# Prerequisites

Before you can install and connect the sensors, make sure of the following:

* Optional: copy your public SSH key to your Pi for [Passwordless SSH access]
* I2C must be enabled. See [Enabling I2C]
* The station-monitoring-service is running. See [running the Station Monitoring Service]
* The station exists in the service and contains the sensors that you plan to connect to it.

# Installation

Learn how to connect the sensor and install the Station Client.

1. Login to your Pi via SSH

2. Create [virtual env]

   The virtual env will contain all the software needed to run the station-client in a nicely isolated and dedicated environment, so it
   won't interfere with anything else on the system.

    ```shell script
    cd ~
    mkdir rcm && cd rcm
    python3 -m venv venv
    source venv/bin/activate
    ```
   (1): Optional: Navigate to the home folder, just in case you were in another directory unintentionally.

   (2): Creates the directory `rcm` and navigate into it. This will be the folder containing everything related to the Residential Climate
   Monitoring project.

   (3): Create a virtual env with the name `venv`. All the necessary python package will end up here.

   (4): Activate the virtual env.

3. Install Station Client

   To install the package:

   ```shell script
   pip install rcm-station-client
   ```

   Alternatively, you can also directly clone it if you have a fork or want to make customizations:

    ```shell script
    git clone https://gitlab.com/residential-climate-monitoring/station-client.git
    cd station-client
    pip install -r requirements.txt
    ```

# Configuration

The Station Client requires some configuration settings before it will work.

* Create .env file

  All the configuration will be read from a `.env` file. Create it in the root of the "rcm" folder you created during installation. After
  this step your directory structure should look like this:
    ```
    rcm/
    - .env
    - venv/
    ```

  _Note: if you cloned the repo, you must edit the .env file of the project: "rcm/station-client/.env" directly._

* Configure station settings

  Copy and paste the following into the file:

    ```shell script
    station-name=test
    api-base-url=https://raspberrypi.local:8080
    ``` 

  `station-name` - Configure the name of the station, typically the location where it is located. E.g. 'living-room'. This must match with
  the name of the station as it is registered in the Station Monitoring Service.

  `api-base-url` - This is the location where the station monitoring service API is available on. Change "raspberry" to the hostname and/or
  change "raspberry.local" to the IP address of the raspberry that runs the Station Monitoring Service to match your environment. The port
  and http scheme can and should also be changed accordingly to match your environment.

* Configure security settings

  Security is enabled by default on both the client and server side. You can create a free account on [Auth0] to obtain the necessary
  settings, or disable security. If you have an Auth0 account you will need your application client id, client secret, audience and tenant +
  zone.

  To disable security, add the following:

    ```shell script
    auth-enabled=false
    ```

  Note: Below settings only apply when auth-enabled=true!

  To configure with Auth0, add the following:

    ```shell script
    auth-client-id=
    auth-client-secret=
    auth-audience=
    auth-token-endpoint=https://${auth0-tenant}.${auth0-region}.auth0.com/oauth/token    
    ```

  `auth-client-id` - In Auth0 you'll have to create an application, which will represent the Residential Climate Monitoring system. Put the
  client-id here.

  `auth-client-secret` - This is the secret, make sure this token is safe and access to the file and system is limited to "authorized
  personnel" only!

  `auth-audience` - This is the identifier of the API, that you created as part of your Auth0 application. This should match with the
  station monitoring service.

  `auth-token-endpoint` - This is the endpoint that will be called by the Station Client to obtain an M2M token. Replace it with your tenant
  and region.

  Note: You may need to change the Token Expiration in Auth0 because the token endpoint has a quota of 1.000 requests / month. If you intend
  to run the client regularly (see usage section) then you will quickly exceed this quota, especially if you have multiple stations running.
  The Station Client caches the token by writing it to a file along with the timestamp when it will expire and request a new one only when
  it is expired. Setting the Token Expiration to 86400 seconds (24 hours) will allow you to connect up to 32 stations before hitting the
  quota.

* Configure for testing/development on a machine without I2C

  To disable the I2C altogether and avoid exceptions when running the client on systems without a I2C bus, configure the following:

  ```shell
  disable-i2c=true
  ```
  Note: sensors that depend on I2C are not supported while I2C is disabled.

## Sensor specific configuration

Some sensors allow for customization. Below you can find more details for each sensor.

* **BME680**

  The sensor can be calibrated with sea level pressure to calculate the current altitude. This is not implemented yet, stay tuned.


* **SHT31-D**

  The SHT31-D has two modes: `Single` and `Periodic`. Currently, it only supports Single (default) mode.

  The sensor also comes with a heater than can be turned on to evaporate any condensation. It is planned to turn on the heater automatically
  in the future if humidity levels exceed a certain threshold. Stay tuned.

  To use the secondary address, add the following to the sensor settings:

  ```json
  {
    "secondary_address": "true"
  }
  ```

* **TSL2591**

  The TSL2591 has configurable `gain` and `integration time` for various lighting conditions. Learn more about [Gain and timing]. See
  the [TSL2591 reference sheet] for an overview of values you can expect in different conditions.

  Add the following to the `.env` file to adjust gain and/or timing:

    ```shell script
    tsl2591-gain=GAIN_MEDIUM
    tsl2591-integration-time=100MS
    ```

  `tsl2591-gain` - Sets the gain level, the higher the level the more the signal will be "amplified". Low light conditions requires more
  gain to be measurable.

  Supported values are:

  * `GAIN_LOW` - Sets the gain to 1x (bright light)
  * `GAIN_MEDIUM` - Sets the gain to 25x (general purpose) - default
  * `GAIN_HIGH` - Sets the gain to 428x (low light)
  * `GAIN_MAX` - Sets the gain to 9876x (extremely low light)

  `tsl2591-integration-time` - Set the integration time, a higher value allows the sensor to "capture" more light.

  Supported values are:

  * `100MS` - 100 milliseconds - default
  * `200MS` - 200 milliseconds
  * `300MS` - 300 milliseconds
  * `400MS` - 400 milliseconds
  * `500MS` - 500 milliseconds
  * `600MS` - 600 milliseconds


* **SGP30**

  The SGP30 requires calibration before it can be used.

  ```shell
    sgp30-init-baseline=true
    sgp30-baseline-file=/home/pi/rcm-sgp30-baseline.txt
  ```

  * `sgp30-init-baseline` - Set this to true to calibrate the sensor and write the baseline file to the baseline file.
  * `sgp30-baseline-file` - The path to the file where the baseline values are stored.

# Hardware installation

After the software is installed and configured, it is time to connect the sensor(s):

|RPIO         |Sensor    |
|-------------|----------|
|3.3v         |VIN       |
|GND          |GND       |
|GPIO 2 (SDA) |SDA [1]   | 
|GPIO 3 (SCL) |SCL [2]   |

Note 1: On the BME680 this pin is called "SDI" instead. \
Note 2: On the BME680 this pin is called "SCK" instead.

## Addresses

The I2C addresses are listed below:

|Sensor  | Address | Secondary Address |
|--------|---------|-------------------|
|BME680  |0x77     |                   |
|SHT31-D |0x44     |0x45               |
|TSL2591 |0x29     |                   |
|SGP30   |0x58     |                   |

Note: To use the secondary address, see sensor specific configuration.

# Calibration

This section describes how to calibrate sensors. This should be done once before first usage.

* **SGP30**

  Set the `sgp30-init-baseline` property to true in the .env file and run the station_client manually once and leave it running for at least
  one hour, ideally 12 hours. Each hour it will write the baseline values to the baseline file. Once this process is finished, and the file
  is ready you can switch the property back to false or comment it out and run the script as described below.

# Usage

To run the station client manually, run:

```shell script
python station_client.py
```

To run the station client periodically, configure it using [Crontab]:

To edit crontab settings:

```shell script
crontab -e
```

```shell script
* * * * * /home/pi/rcm/venv/bin/python3 /home/pi/rcm/venv/lib/python3.7/site-packages/rcm/station_client.py
```

_Note: if you cloned the repo, you must change the path accordingly, e.g.: "* * * * * /home/pi/rcm/venv/bin/python3
/home/pi/rcm/station-client/rcm/station_client.py_

The `* * * * *` expression executes the script once every minute. The `0 0 * * *` expression executes the script once a day at midnight.

```
# * * * * *  command to execute
# ┬ ┬ ┬ ┬ ┬
# │ │ │ │ └─ day of week (0 - 7) (0 to 6 are Sunday to Saturday, or use names; 7 is Sunday, the same as 0)
# │ │ │ └─ month (1 - 12)
# │ │ └─ day of month (1 - 31)
# │ └─ hour (0 - 23)
# └─ min (0 - 59)
```

# Troubleshooting

To troubleshoot, the logs can be found at: `/home/pi/rcm-station-client.log`

[Passwordless SSH access]: https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md

[Enabling I2C]: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

[running the Station Monitoring Service]: https://gitlab.com/residential-climate-monitoring/station-monitoring-service

[virtual env]: https://docs.python.org/3/tutorial/venv.html

[gpiozero]: https://gpiozero.readthedocs.io/en/stable/cli_tools.html

[Auth0]: https://auth0.com

[Gain and timing]: https://learn.adafruit.com/adafruit-tsl2591/wiring-and-test#gain-and-timing-762936-18

[Crontab]: https://www.raspberrypi.org/documentation/linux/usage/cron.md

[TSL2591 reference sheet]: https://gitlab.com/residential-climate-monitoring/station-client/-/blob/master/TSL2591_REFERENCE.md