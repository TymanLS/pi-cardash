# Pi Car Dash
A Raspberry Pi based car dashboard. This script is designed for use with a Bluetooth OBDII adapter like the one [here](https://www.amazon.com/Veepeak-Bluetooth-Diagnostic-Supports-Vehicles/dp/B076XVQMVS/ref=sr_1_4?keywords=veepeak&qid=1585593711&sr=8-4), but it should also work with ELM327 OBDII adapters connected through USB or other serial protocols. The directions assume that Raspbian is the installed OS.

## Installation
These programs require Python 3 to be installed. It can be installed on Raspbian with:

```bash
$ sudo apt install python3
```

These programs also make use of the `python-OBD` module, which can be installed using `pip3` with:

```bash
$ pip3 install obd
```

If this does not work, it may be necessary to install the module to the Python user directory with:

```bash
$ pip3 install --user obd
```

If using a Bluetooth adapter, ensure that the Bluetooth stack is installed. It can be installed on Raspbian with:

```bash
$ sudo apt install bluez
```


## Bluetooth Setup
In order to use a Bluetooth OBDII adapter, it must be paired and connected to the Raspberry Pi as an RFCOMM serial device

### Bluetooth Pairing
The OBDII adapter must first be paired with the Raspberry Pi to enable the proper connection.

On the Raspberry Pi, make sure the Bluetooth adapter is not blocked by `rfkill`

```
$ rfkill list
1: hci0: Bluetooth
        Soft blocked: no
        Hard blocked: no
```

If it is blocked, unblock it.

```
$ rfkill unblock bluetooth
```

Then, enable Bluetooth and attempt to scan for the OBDII adapter with `bluetoothctl`. The adapter may need to be plugged into a vehicle in order to be powered and discoverable.

```
$ sudo bluetoothctl
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# default-agent
[bluetooth]# scan on 
```

Take note of the MAC address of the Bluetooth OBDII adapter. It should be in the form `xx:xx:xx:xx:xx:xx`.

```
[NEW] Device 11:22:33:44:55:66 OBDII Adapter
```
Once the MAC address is known, stop scanning and pair with the adapter.

```
[bluetooth]# scan off
[bluetooth]# pair <MAC address of OBDII adapter>
[bluetooth]# trust <MAC address of OBDII adapter>
```

If the pairing process succeeded, the adapter should appear in `bluetoothctl`.

```
[bluetooth]# paired-devices
Device 11:22:33:44:55:66 OBDII Adapter
```

### Setting up RFCOMM Device
After the Bluetooth OBDII adapter is paired, it must be connected as a serial device through RFCOMM.

Ensure that the OBDII adapter is not connected through a normal Bluetooth profile, since this may interfere with connection through RFCOMM.

```
[bluetooth]# disconnect <MAC address of OBDII adapter>
```

Then, bind the OBDII adapter as an RFCOMM device.

```
$ sudo rfcomm bind /dev/rfcomm0 <MAC address of OBDII adapter>
```

This will create a virtual serial device at `/dev/rfcomm0` on channel 1 (default RFCOMM channel). Since the OBDII adapter is now bound to this device, a serial connection will be automatically attempted when the application tries to open the device for data.

#### Manual serial connection
When the device is bound, a connection will be attempted when a device tries to open the virtual serial device. It is also possible to manually connect to the device without binding to see if a connection can be properly established, or for troubleshooting purposes.

```
$ sudo rfcomm connect /dev/rfcomm0 <MAC address of OBDII adapter>
```

Raw serial data can then be read and written to the device using a serial communication program like `minicom`.

#### Automatically bind on startup
RFCOMM bindings are not persistent between restarts of the Raspberry Pi. In order to automatically bind the OBDII adapter to the virtual serial device upon startup, a systemd service unit can be used to run the `rfcomm bind` command after Bluetooth services have started. The provided `obdbind.service` file in [this directory](obdbind/) is a simple implementation of this.

#### Deprecation of `rfcomm` tool
The `rfcomm` utility used to create a virtual serial device has been deprecated by BlueZ (official Linux Bluetooth stack). However no upstream replacement utilities provide the same functionality as `rfcomm`, so this setup requires the usage of this outdated tool until a proper replacement is provided.


## Usage
Running the program will automatically connect to the a serial device and attempt to connect to it as an OBDII adapter.

```
$ ./car_stat.py
```

If the serial device for the OBDII adapter is known, it can be specified as an argument.

```
$ ./car_stat.py /dev/rfcomm0
```

If synchronous querying is desired, launch the synchronous version of the program instead.

```bash
$ ./car_stat_sync.py
```

Note: the synchronous version of the program currently always uses `/dev/rfcomm0` as the OBDII device
**TODO: add arguments to the synchronous version of the program**
