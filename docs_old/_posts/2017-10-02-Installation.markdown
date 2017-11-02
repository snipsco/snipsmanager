---
layout: page
title:  "Installation"
date:   2017-10-02 12:53:25 +0200
permalink: /installation/
---

Sam run on Raspbian and macOS. The latter platform is intended mainly for developing skills, but it does not run the Snips Platform yet.

## Raspberry Pi

On Raspbian, Sam can be installed in three ways: either with the custom Snips Raspbian image, which includes all the libraries necessary to run both the Snips Platform, and Sam itself. It also comes preinstalled with a Bluetooth service, allowing you to control the Raspberry Pi direclty with your phone via the [iOS App]({{ site.baseurl }}/{% post_url 2017-10-02-iOS-App %}).

### Raspbian image

Download the [Snips Raspbian Image]() and burn it to an SD card, for instance using [Etcher](https://etcher.io). Insert the SD card in your Raspberry Pi, and boot.

In order to get your Raspberry Pi connected to your Wi-Fi network, you can use the companion [iOS App]({{ site.baseurl }}/{% post_url 2017-10-02-iOS-App %}). Alternatively, you can follow the [instructions](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) on the Raspberry Pi website.

### Debian package

If you already have a working Raspberry Pi setup, you can install Sam using `apt-get`. You will first need to update the Debian package repository:

- Create a file `/etc/apt/source.list.d/snips.list` (we use `snips.list` here, but any name will work)
- Add the following line: `deb https://s3.amazonaws.com/snips-deb/ stable main`
- Run `sudo apt-get update` to update the repository

Sam can now be installed:

```sh
$ sudo apt-get install snipsskills
```

### Python package

Sam also comes as a `pip` package. This however requires installing a few dependencies beforehand. Start by running:

```sh
$ sudo apt-get update
$ sudo apt-get install python-pip libsdl-mixer1.2 libusb-1.0 \
    python-pyaudio libsdl1.2-dev cython cython3 libudev-dev \
    python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev libsmpeg-dev python-numpy libportmidi-dev \
    libswscale-dev libavformat-dev libavcodec-dev \
    portaudio19-dev nodejs build-essential -y
```

Next, we want to create a Python virtual environment to avoid conflicts with existing dependencies, and to be able to run Sam without root privileges:

```sh
$ sudo pip install --upgrade virtualenv
$ virtualenv --python=/usr/bin/python2.7 sam-env
$ source sam-env/bin/activate
(sam-env) $ pip install pip --upgrade
```

You may replace `sam-env` with any name for your virtual environment.

We are ready to install the `sam` package:

```sh
(sam-env) $ pip install sam
```

## macOS

On macOS, Sam is also available as a `pip` package. To install, Portaudio, Pyaudio and SDL are needed:

```sh
$ sudo easy_install pip
$ brew install portaudio
$ brew install sdl
$ pip install --global-option='build_ext' \
    --global-option='-I/usr/local/include' \
    --global-option='-L/usr/local/lib' pyaudio
```

Next, like with Raspbian, we create a Python virtual environment in which Sam will be run:

```sh
$ sudo pip install --upgrade virtualenv
$ virtualenv --python=/usr/bin/python2.7 sam-env
$ source sam-env/bin/activate
(sam-env) $ pip install pip --upgrade
```

Sam can now be installed.

```sh
(sam-env) $ pip install sam
```
