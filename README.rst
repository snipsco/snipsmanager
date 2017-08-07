Snips Skills Manager
====================

|Build Status| |PyPI| |MIT License|

The Snips Skills Manager is a tool for easily setting up and managing a Snips assistant.

A single configuration file, the `Snipsfile <https://github.com/michaelfester/awesome-snips/>`_, is required to create a Snips assistant. In it, you specify:

- The URL of your assistant, as created in the `Snips Console <https://console.snips.ai>`_
- The `skills <https://github.com/michaelfester/awesome-snips/>`_ you want to install
- Bindings between intents and skills
- If required, additional parameters for you skill, such as an API key or the address of a lamp
- Various configuration parameters, such as language and logging preferences.

Check out `Awesome Snips <https://github.com/michaelfester/awesome-snips/>`_, a curated list of Snips skills, assistants and other resources to get you started. In particular, make sure to read the `Getting Started guide <https://github.com/michaelfester/awesome-snips/>`_.

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
