# obdbind
This is a simple systemd service unit that is designed to run bind a Bluetooth OBDII adapter on startup.

## Installation
The provided script will automatically install the obdbind.service unit file in `/lib/systemd/system` and enable it. Run it with `sudo` in this directory:

```bash
$ sudo ./install_obdbind.sh install <MAC address of the OBDII adapter>
```

To disable and remove the unit file:

```bash
$ sudo ./install_obdbind.sh uninstall
```

## obdbind.service
This systemd service unit will simply run the `rfcomm bind` command on startup to bind the Bluetooth OBDII adapter to an RFCOMM virtual serial device.

```bash
$ rfcomm bind /dev/rfcomm0 <MAC address of the OBDII adapter>
```

The unit file can be modified to bind to a different RFCOMM virtual serial device (e.g. `/dev/rfcomm9`), or to bind to a specific RFCOMM channel. These are specified in `Environment=` directives, and can be easily modified.

```
Environment="OBD_RFCOMM_DEV=/dev/rfcomm9"
Environment="OBD_MAC_ADDR=AA:BB:CC:DD:EE:FF"
Environment="OBD_RFCOMM_CHANNEL=5"
```

