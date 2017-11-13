# Snips Manager

[![Build Status](https://travis-ci.org/snipsco/snipsmanager.svg)](https://travis-ci.org/snipsco/snipsmanager)
[![PyPi](https://img.shields.io/pypi/v/snipsmanager.svg)](https://pypi.python.org/pypi/snipsmanager)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/snipsco/snipsmanager/master/LICENSE.txt)

The Snips Manager is a tool for easily setting up and managing a [Snips](https://www.snips.ai) assistant.

A single configuration file, the [Snipsfile](https://github.com/michaelfester/awesome-snips/), is required to create a Snips assistant. In it, you specify:

- The URL of your assistant, as created in the [Snips Console](https://console.snips.ai)
- The [skills](https://github.com/michaelfester/awesome-snips/) you want to install
- Bindings between intents and skills
- If required, additional parameters for you skill, such as an API key or the address of a lamp
- Various configuration parameters, such as language and logging preferences.

Check out [Awesome Snips](https://github.com/michaelfester/awesome-snips/), a curated list of Snips skills, assistants and other resources to get you started. In particular, make sure to read the [Getting Started guide](https://github.com/snipsco/snipsmanager/wiki/Getting-Started).

## Installation

### Debian package

If you already have a working Raspberry Pi setup, you can install Snips Skills using `apt-get`. You will first need to update the Debian package repository:

- Create a file `/etc/apt/sources.list.d/snips.list` (we use `snips.list` here, but any name will work)
- Add the following line: `deb https://s3.amazonaws.com/snips-deb/ stable main`
- Run `sudo apt-get update` to update the repository

Snips Skills can now be installed:

```sh
$ sudo apt-get install snipsskills
```

### Python package

Snips Skills also comes as a `pip` package. This however requires installing a few dependencies beforehand. Start by running:

```sh
$ sudo apt-get update
$ sudo apt-get install python-pip libsdl-mixer1.2 libusb-1.0 \
    python-pyaudio libsdl1.2-dev cython cython3 libudev-dev \
    python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev libsmpeg-dev python-numpy libportmidi-dev \
    libswscale-dev libavformat-dev libavcodec-dev \
    portaudio19-dev nodejs build-essential -y
```

Next, we want to create a Python virtual environment to avoid conflicts with existing dependencies, and to be able to run Snips Skills without root privileges:

```sh
$ sudo pip install --upgrade virtualenv
$ virtualenv --python=/usr/bin/python2.7 snipsskills-env
$ source snipsskills-env/bin/activate
(snipsskills-env) $ pip install pip --upgrade
```

You may replace `snipsskills-env` with any name for your virtual environment.

We are ready to install the `snipsskills` package:

```sh
(snipsskills-env) $ pip install snipsskills
```

## macOS

On macOS, Snips Skills is also available as a `pip` package. To install, Portaudio, Pyaudio and SDL are needed:

```sh
$ sudo easy_install pip
$ brew install portaudio
$ brew install sdl
$ pip install --global-option='build_ext' \
    --global-option='-I/usr/local/include' \
    --global-option='-L/usr/local/lib' pyaudio
```

Next, like with Raspbian, we create a Python virtual environment in which Snips Skills will be run:

```sh
$ sudo pip install --upgrade virtualenv
$ virtualenv --python=/usr/bin/python2.7 snipsskills-env
$ source snipsskills-env/bin/activate
(snipsskills-env) $ pip install pip --upgrade
```

Snips Skills can now be installed.

```sh
(snipsskills-env) $ pip install snipsskills
```

<!-- 
Snips Manager is available as an `apt-get` package. To install it, first add the Snips repository to your list of `apt-get` sources. In the folder `/etc/apt/sources.list.d`, create a file called `snips.list`, and add the line:

```
deb https://s3.amazonaws.com/snips-deb/ stable main
```

Then run:

```sh
$ sudo apt-get update
$ sudo apt-get install snipsmanager
```
 -->

## Usage

### Creating the Snipsfile

Start your project by creating a `Snipsfile`, which is where all the configuration is set. This is a simple text file, adhering to the [YAML](https://en.wikipedia.org/wiki/YAML) format. Here is a basic configuration:

```yaml
assistant_url: <YOUR ASSISTANT URL>
locale: en_US
logging: True
default_location: Paris,fr
skills:
  - package_name: snipshue
    class_name: SnipsHue
    url: https://github.com/snipsco/snips-skill-hue
    params:
      hostname: <PHILIPS HUE IP>
      username: <PHILIPS HUE USERNAME>
      light_ids: [1, 2, 3, 4, 5, 6]
    intents:
      - intent: ActivateLightColor
        action: "turn_on"
      - intent: DeactivateObject
        action: "turn_off"
```

For further explanations and examples, check out our [Snipsfile Wiki](https://github.com/snipsco/snipsmanager/wiki/The-Snipsfile).

### Installing the skills

Next, setup the system by running the `install` command:

```sh
$ snipsmanager install
```

### Launching the skills server

If you enabled Snips Manager to run on boot, simply reboot your device. Otherwise, start the service manually by running:

```sh
$ snipsmanager run
```

## Contributing

Please see the [Contribution Guidelines](https://github.com/snipsco/snipsmanager/blob/master/CONTRIBUTING.rst).

## Copyright

This skill is provided by [Snips](https://www.snips.ai) as Open Source software. See [LICENSE.txt](https://github.com/snipsco/snipsmanager/blob/master/LICENSE.txt) for more information.
