#!/bin/sh

### Function to print the help message
print_help () {
	echo "Usage: ./install_obdbind.sh install <OBDII adapter MAC address>"
	echo "       ./install_obdbind.sh uninstall"
}

### Parse arguments
# Check if installing or uninstalling
if [ "$1" = "uninstall" ]; then
	uninstall=true
elif [ "$1" = "install" ]; then
	uninstall=false
else
	print_help
	exit 1
fi

# Check if a valid MAC address is given when installing
if [ "$uninstall" = false ]; then
	if  (echo "$2" | grep -Eq '^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$'); then
		btadapter=$2
	else
		echo "Invalid MAC address"
		print_help
		exit 1
	fi
fi

### Check if running with sudo
if [ "$(id -u)" != "0" ]; then
	echo "Must be run as root to install obdbind.service, exiting..."
	exit 1
fi

# Check if uninstalling
if [ "$uninstall" = true ]; then
	### Uninstalling obdbind.service
	# Check whether obdbind exists on the system
	if ! (systemctl list-units --full --all | grep -Fq 'obdbind.service'); then
		echo "obdbind is not installed"
		exit 0
	fi

	# Disable obdbind.service
	echo "Disabling obdbind.service ..."
	systemctl disable obdbind.service || { echo "Failed to disable obdbind.service"; exit 2; }

	# Remove obdbind.service from /lib/systemd/system
	echo "Deleting obdbind.service from /lib/systemd/system ..."
	rm /lib/systemd/system/obdbind.service || { echo "Failed to delete obdbind.service"; exit 2; }

	# Reload systemd manager configuration
	echo "Reloading systemd daemon ..."
	systemctl daemon-reload || { echo "Failed to reload systemd daemon"; exit 2; }

	echo "obdbind.service has been successfully uninstalled!"
else
	### Installing obdbind.service
	# Copy obdbind.service unit file to /lib/systemd/system
	echo "Copying service unit file to /lib/systemd/system ..."
	cp ./obdbind.service /lib/systemd/system/obdbind.service || { echo "Failed to copy obdbind.service"; exit 2; }

	# Replace the MAC address in the file with the new one given
	sed -i "s/11:22:33:44:55:66/$btadapter/g" /lib/systemd/system/obdbind.service || { echo "Failed to set the new MAC address"; exit 2; }

	# Reload systemd manager configuration
	echo "Reloading systemd daemon ..."
	systemctl daemon-reload || { echo "Failed to reload systemd daemon"; exit 2; }

	# Enable obdbind.service
	echo "Enabling obdbind.service ..."
	systemctl enable obdbind.service || { echo "Failed to enable obdbind.service"; exit 2; }

	echo "obdbind.service has been successfully installed!"
fi

