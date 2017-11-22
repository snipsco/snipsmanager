# Snips Manager

[![Build Status](https://travis-ci.org/snipsco/snipsmanager.svg)](https://travis-ci.org/snipsco/snipsmanager)
[![PyPi](https://img.shields.io/pypi/v/snipsmanager.svg)](https://pypi.python.org/pypi/snipsmanager)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/snipsco/snipsmanager/master/LICENSE.txt)

The Snips Manager is a tool for easily setting up and managing a [Snips](https://www.snips.ai) assistant.

A single configuration file, the [Snipsfile](https://github.com/snipsco/snipsmanager/wiki/The-Snipsfile), is required to create a Snips assistant. In it, you specify:

- The URL of your assistant model, as created in the [Snips Console](https://console.snips.ai)
- The [lambdas](https://github.com/snipsco/snipsmanager/wiki/Creating-a-Lambda) you want to install
- Bindings between intents and lambdas
- If required, additional parameters for your lambdas, such as an API key or the address of a lamp
- Various configuration parameters, such as language and logging preferences.

Check out [Awesome Snips](https://github.com/snipsco/awesome-snips), a curated list of Snips assistants, lambdas and other resources to get you started.

## Installation

### Debian package

Snips Manager is available as an `apt-get` package. To install it, run the following:

```sh
$ sudo apt-get update
$ sudo apt-get install -y dirmngr
$ sudo bash -c 'echo "deb https://raspbian.snips.ai/$(lsb_release -cs) stable main" > /etc/apt/sources.list.d/snips.list'
$ sudo apt-key adv --keyserver pgp.mit.edu --recv-keys D4F50CDCA10A2849
$ sudo apt-get update
$ sudo apt-get install -y snipsmanager
```

### Python package

Snips Manager also comes as a `pip` package. This however requires installing a few dependencies beforehand. Start by running:

```sh
$ sudo apt-get update
$ sudo apt-get install python-pip libsdl-mixer1.2 libusb-1.0 \
    python-pyaudio libsdl1.2-dev cython cython3 libudev-dev \
    python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev libsmpeg-dev python-numpy libportmidi-dev \
    libswscale-dev libavformat-dev libavcodec-dev \
    portaudio19-dev nodejs build-essential -y
```

Next, create a Python virtual environment to avoid conflicts with existing dependencies, and to be able to run Snips Manager without root privileges:

```sh
$ sudo pip install --upgrade virtualenv
$ virtualenv --python=/usr/bin/python2.7 snips
$ source snips/bin/activate
(snips) $ pip install pip --upgrade
```

You may replace `snips` with any name for your virtual environment.

We are ready to install the `snipsmanager` package:

```sh
(snips) $ pip install snipsmanager
```

## macOS

On macOS, Snips Manager is also available as a `pip` package. To install, Portaudio, Pyaudio and SDL are needed:

```sh
$ sudo easy_install pip
$ brew install portaudio
$ brew install sdl
$ pip install --global-option='build_ext' \
    --global-option='-I/usr/local/include' \
    --global-option='-L/usr/local/lib' pyaudio
```

Next, like with Raspbian, we create a Python virtual environment in which Snips Manager will be run:

```sh
$ sudo pip install --upgrade virtualenv
$ virtualenv --python=/usr/bin/python2.7 snips
$ source snips/bin/activate
(snips) $ pip install pip --upgrade
```

Snips Manager can now be installed:

```sh
(snips) $ pip install snipsmanager
```

## Usage

### Creating the Snipsfile

Start your project by creating a `Snipsfile`, which is where all the configuration is set. This is a simple text file, adhering to the [YAML](https://en.wikipedia.org/wiki/YAML) format. Here is a basic configuration:

```yaml
assistant_url: <YOUR ASSISTANT URL>
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

### Installing the lambdas

Next, setup the assistant by running the `install` command:

```sh
$ snipsmanager install
```

The `snipsmanager` service will automatically start on boot. You can also start it manually by running:

```sh
$ snipsmanager run
```

## Contributing

Please see the [Contribution Guidelines](https://github.com/snipsco/snipsmanager/blob/master/CONTRIBUTING.md).

## Copyright

This skill is provided by [Snips](https://www.snips.ai) as Open Source software. See [LICENSE.txt](https://github.com/snipsco/snipsmanager/blob/master/LICENSE.txt) for more information.
