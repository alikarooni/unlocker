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

echo "Get macOS VMware Tools 3.0.4"
echo "==============================="
echo "(c) Dave Parsons 2015-18"

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

pyversion=""
pipversion=""
if command -v python &> /dev/null; then
    pyversion="python"
    pipversion="pip"
elif command -v python3 &> /dev/null; then
    pyversion="python3"
    pipversion="pip3"
else
    echo "python could not be found"
    exit
fi

# Check if pip or pip3 is installed, install if necessary
if ! command -v $pipversion &> /dev/null; then
    install_pip $pipversion
fi

# Check if requests is already installed
if ! check_requests_installed $pyversion; then
    # Install requests
    install_requests $pipversion
fi

echo Getting VMware Tools...
$pyversion gettools.py
cp ./tools/darwin*.* /usr/lib/vmware/isoimages/

echo Finished!

