#!/bin/bash

# Function to install pip if not installed
install_pip() {
    if [[ "$1" == "pip" ]]; then
        echo "Installing pip..."
        sudo apt-get update
        sudo apt-get install -y python-pip
    elif [[ "$1" == "pip3" ]]; then
        echo "Installing pip3..."
        sudo apt-get update
        sudo apt-get install -y python3-pip
    fi
}

# Function to check if requests is installed for a given python version
check_requests_installed() {
    $1 -c "import requests" &> /dev/null
    return $?
}

# Function to install requests for a given pip
install_requests() {
    echo "Installing requests using $1..."
    $1 install requests

    # Verify installation
    if python -c "import requests" &> /dev/null || python3 -c "import requests" &> /dev/null
    then
        echo "Requests successfully installed."
    else
        echo "Failed to install requests."
    fi
}

set -e

echo "Unlocker 3.0.4 for VMware Workstation"
echo "====================================="
echo "(c) Dave Parsons 2011-18"

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo Creating backup-linux folder...
rm -rf ./backup-linux
mkdir -p "./backup-linux"
cp -v /usr/lib/vmware/bin/vmware-vmx ./backup-linux/
cp -v /usr/lib/vmware/bin/vmware-vmx-debug ./backup-linux/
cp -v /usr/lib/vmware/bin/vmware-vmx-stats ./backup-linux/
if [ -d /usr/lib/vmware/lib/libvmwarebase.so.0/ ]; then
    cp -v /usr/lib/vmware/lib/libvmwarebase.so.0/libvmwarebase.so.0 ./backup-linux/
elif [ -d /usr/lib/vmware/lib/libvmwarebase.so/ ]; then
    cp -v /usr/lib/vmware/lib/libvmwarebase.so/libvmwarebase.so ./backup-linux/
fi

source ./lnx-check-python.sh

echo Patching...
$pyversion ./unlocker.py

echo Getting VMware Tools...
$pyversion gettools.py
cp ./tools/darwin*.* /usr/lib/vmware/isoimages/

echo Finished!
