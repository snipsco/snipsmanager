Snips Skills Manager
====================

|Build Status| |PyPI| |MIT License|


The Snips Skills Manager is a tool for easily setting up and managing a Snips assistant.

A single configuration file, the Snipsfile, is required to create a Snips assistant. In it, you specify:

- The URL of your assistant, as created in the `Snips Console <https://console.snips.ai>`_
- The `skills <https://github.com/michaelfester/awesome-snips/>`_ you want to install
- If required, additional parameters for you skill, such as an API key, or the IP address of a lamp
- A simple set of rules which tell how skills should react to incoming intents
- Various configuration parameters, such as language and logging preferences.

Check out `Awesome Snips <https://github.com/michaelfester/awesome-snips/>`_, a curated list of Snips skills, assistants and other resources to get you started. In particular, make sure to read the `Getting Started guide <https://github.com/michaelfester/awesome-snips/>`_.

Installation
------------

The Snips Skills Manager is on `PyPI <https://pypi.python.org/pypi/snipsskills>`_, so you can just install it with `pip <http://www.pip-installer.org>`_:

.. code-block:: console

    $ pip install snipsskills

Usage
-----

Start by creating a ``Snipsfile``, which is where all the configuration is set. This is a simple text file, adhering to the YAML format. Here is a basic configuration:

.. code-block:: yaml

    assistant: SNIPS_ASSISTANT_URL
    locale: en_US
    logging: True
    default_location: Paris,fr
    skills:
      - package_name: snipshue
        class_name: SnipsHue
        pip: snipshue=0.1.2
        params:
          hostname: PHILIPS_HUE_IP
          username: PHILIPS_HUE_USERNAME
          light_ids: [1, 2, 3, 4, 5, 6]
        intents:
          - intent: DeactivateObject
            action: "turn_off"
          - intent: ActivateLightColor
            action: "turn_on"

For further explanations and examples, check out our `Snipsfile Wiki <https://github.com/michaelfester/awesome-snips/>`_.

Next, setup the system by running the ``install`` command:

.. code-block:: console

    $ snipsskills install

We are now ready to start the service, using the ``run`` command:

.. code-block:: console

    $ snipsskills run

Copyright
---------

This skill is provided by `Snips <https://www.snips.ai>`_ as Open Source software. See `LICENSE.txt <https://github.com/snipsco/snips-skill-smartercoffee/blob/master/LICENSE.txt>`_ for more
information.

.. |Build Status| image:: https://travis-ci.org/snipsco/snipsskills.svg
   :target: https://travis-ci.org/snipsco/snipsskills
   :alt: Build Status
.. |PyPI| image:: https://img.shields.io/pypi/v/snipsskills.svg
   :target: https://pypi.python.org/pypi/snipsskills
   :alt: PyPI
.. |MIT License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/snipsco/snipsskills/master/LICENSE.txt
   :alt: MIT License
