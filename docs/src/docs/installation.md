---
title: Installation
---

Snips Skills is currently available on [Raspbian](https://www.raspberrypi.org/downloads/raspbian/), and will soon also be available on macOS.

#### Snips Raspbian image

Snips Skills is part of the [Snips Raspbian image](https://www.snips.ai/snips_raspbian_lite.zip). To install it:

- Download the Snips Raspbian image
- Flash it to an SD card (e.g. using [Etcher](https://etcher.io))
- Insert the SD card in your Raspberry Pi and turn it on

#### Debian package

Snips Skills is available as an `apt-get` package. To install it, first add the Snips repository to your list of `apt-get` sources. Edit `/etc/apt/sources.list` and add the line:

```sh
deb http://archive.raspbian.org/raspbian/ stretch main
```

The run

```sh
$ apt-get install snipsskills
```

#### Pip package

Alternatively, Snips Skills comes as a [pip](https://pypi.python.org/pypi/pip) package, distributed on [PyPi](https://pypi.python.org/pypi/snipsskills):

```sh
$ pip install snipsskills
```

We recommend running this in a [virtual environment](https://virtualenv.pypa.io/en/latest/) to avoid overriding existing setups and granting root privileges:

```sh
$ sudo pip install --upgrade virtualenv
$ virtualenv --python=/usr/bin/python2.7 snips
$ source snips/bin/activate
(snips) $ pip install pip --upgrade
(snips) $ pip install snipsskills
```

Depending on your setup, you may need to install some dependencies via `apt-get`:

```sh
$ sudo apt-get install python-pip libsdl-mixer1.2 libusb-1.0 python-pyaudio libsdl1.2-dev cython libudev-dev python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev python-numpy libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev portaudio19-dev nodejs build-essential
```

#### Homebrew package (coming soon)

On macOS, Snips Skills is available as a [Homebrew](https://brew.sh/) package:

```sh
$ brew install snipsskills
```


<!-- 
Installation
------------

We suggest installing and running Snips Skills using a `virtualenv <https://virtualenv.pypa.io/en/latest/>`_ to avoid granting root privileges, and ensure your setup does not break when other packages are installed:

.. code-block:: console

  $ sudo pip install --upgrade virtualenv
  $ virtualenv --python=/usr/bin/python2.7 snips
  $ source snips/bin/activate

You may exit the virtualenv by running ``deactivate``.

We are now ready to install the `snipsskills <https://pypi.python.org/pypi/snipsskills>`_ package. Make sure ``pip`` is up to date:

.. code-block:: console

  $ pip install pip --upgrade
  $ pip install snipsskills

Installing without virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you do not wish to use a virtualenv, you need to run the pip commands with root privileges:

.. code-block:: console

  $ sudo pip install pip --upgrade
  $ sudo pip install snipsskills
 -->