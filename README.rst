Snips Manager
=============

|Build Status| |PyPI| |MIT License|

The Snips Manager Manager is a tool for easily setting up and managing a Snips assistant.

A single configuration file, the `Snipsfile <https://github.com/michaelfester/awesome-snips/>`_, is required to create a Snips assistant. In it, you specify:

- The URL of your assistant, as created in the `Snips Console <https://console.snips.ai>`_
- The `skills <https://github.com/michaelfester/awesome-snips/>`_ you want to install
- Bindings between intents and skills
- If required, additional parameters for you skill, such as an API key or the address of a lamp
- Various configuration parameters, such as language and logging preferences.

Check out `Awesome Snips <https://github.com/michaelfester/awesome-snips/>`_, a curated list of Snips skills, assistants and other resources to get you started. In particular, make sure to read the `Getting Started guide <https://github.com/snipsco/snipsmanager/wiki/Getting-Started>`_.

Installation
============

Raspbian
--------

Snips Manager is available as an ``apt-get`` package. To install it, first add the Snips repository to your list of ``apt-get`` sources. In the folder ``/etc/apt/sources.list.d``, create a file called ``snips.list``, and add the line:

.. code-block:: plain

  deb https://s3.amazonaws.com/snips-deb/ stable main

Then run:

.. code-block:: console

  $ sudo apt-get update
  $ sudo apt-get install snipsmanager

macOS
-----

Snips Manager is available on macOS via Homebrew. To install it, simply run:

.. code-block:: plain

  $ brew install snipsmanager

Usage
=====

Creating the Snipsfile
----------------------

Start your project by creating a ``Snipsfile``, which is where all the configuration is set. This is a simple text file, adhering to the `YAML <https://en.wikipedia.org/wiki/YAML>`_ format. Here is a basic configuration:

.. code-block:: yaml

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

For further explanations and examples, check out our `Snipsfile Wiki <https://github.com/snipsco/snipsmanager/wiki/The-Snipsfile>`_.

Installing the skills
---------------------

Next, setup the system by running the ``install`` command:

.. code-block:: console

    $ snipsmanager install

Launching the skills server
---------------------------

If you enabled Snips Manager to run on boot, simply reboot your device. Otherwise, start the service manually by running:

.. code-block:: console

    $ snipsmanager run


Contributing
============

Please see the `Contribution Guidelines <https://github.com/snipsco/snips-skill-hue/blob/master/CONTRIBUTING.rst>`_.


Copyright
=========

This skill is provided by `Snips <https://www.snips.ai>`_ as Open Source software. See `LICENSE.txt <https://github.com/snipsco/snips-skill-smartercoffee/blob/master/LICENSE.txt>`_ for more
information.

.. |Build Status| image:: https://travis-ci.org/snipsco/snipsmanager.svg
   :target: https://travis-ci.org/snipsco/snipsmanager
   :alt: Build Status
.. |PyPI| image:: https://img.shields.io/pypi/v/snipsmanager.svg
   :target: https://pypi.python.org/pypi/snipsmanager
   :alt: PyPI
.. |MIT License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/snipsco/snipsmanager/master/LICENSE.txt
   :alt: MIT License
