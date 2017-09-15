# Texting Dryer Gateway
A Raspberry Pi gateway to receive messages from the [dryer node](https://github.com/makercrew/texting_dryer_node).

## Pre-Setup
### Wire it Up
![Connect the RFM69 to the Pi](schematic/pi_rfm69_bb.png?raw=true)

### Enable SPI
For the gateway code to work you must enable SPI on your Raspberry Pi. The easiest way to do that is by running
```sh
sudo raspi-config
```
Select **Interfacing Options->SPI** and select **Yes**. Exit raspi-config and reboot.

## Quick Start with Docker
The easiest way to get the gateway up and running on the Raspberry Pi is to use the pre-created Docker image.

### Install Docker on the Pi
```sh
curl -sSL https://get.docker.com | sh
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker pi
# Log out and back in to use docker commands
```

### Set Configuration Variables
Modify [env.list](./env.list) to contain your Losant credentials and device ID along with the 16 character encryption key to match your RFM69 node. Be sure to uncomment the lines by removing the '#' from each line.

### Start the Container
Start a new docker container by running the following from the same directory containing **env.list**:
```sh
docker run --privileged --env-file env.list -ti --restart=always --name rfm_gateway makercrew/texting_dryer_gateway
```

## Running Directly on the Pi
If you prefer not to take the Docker route you can run the code directly on your Pi. You should seriously give the Docker route a try though.

### Install Dependencies
```sh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get -qy install build-essential \
                         python-pip \
                         python-dev \
                         python-rpi.gpio \
                         git-core

git clone https://github.com/Gadgetoid/py-spidev
cd py-spidev
make install

pip install paho-mqtt
git clone https://github.com/etrombly/RFM69.git
```

### Set Configuration Variables
Modify [env.list](./env.list) to contain your Losant credentials and device ID along with the 16 character encryption key to match your RFM69 node. Be sure to uncomment the lines by removing the '#' from each line.

### Run the Gateway
```sh
sudo python gateway.py
```

## Playing With The Code
### Running Directly on the Pi
Simply modify [gateway.py](./gateway.py) and run with:

```sh
sudo python gateway.py
```

> **NOTE:** Be sure you have done all of the prerequisite steps found above for running directly on your Pi.

### Building the Docker Image
Modify the code in [gateway.py](./gateway.py) and then re-build the Docker image locally by running:
```sh
docker build -t [name of your new image] .
```

You can now run it in a container with:
```sh
docker run --privileged --env-file env.list -ti --restart=always --name rfm_gateway [name of your new image]
```

