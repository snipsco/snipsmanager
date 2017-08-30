{{project_name}} skill for Snips
======================================

|Build Status| |PyPI| |MIT License|

{{project_name}}

Installation
------------

The skill is on `PyPI`_, so you can just install it with `pip`_:

.. code-block:: console

    $ pip install <PyPi Identifier>

Usage
-----
Snips Skills Manager
^^^^^^^^^^^^^^^^^^^^

It is recommended that you use this skill with the `Snips Skills Manager <https://github.com/snipsco/snipsskills>`_. Simply add the following section to your `Snipsfile <https://github.com/snipsco/snipsskills/wiki/The-Snipsfile>`_:

.. code-block:: yaml

    skills:
    - package_name: {{project_name}}
      pip: <PyPi Identifier>
      requires_tts: True

Standalone usage
^^^^^^^^^^^^^^^^

If you do not wish to use the Snips Skills Manager, it can be used as a standalone Python module. It is on `PyPI`_, so you can just install it with `pip`_:

.. code-block:: console

    $ pip install <PyPi Identifier>

Provide an example here :

.. code-block:: python

    <provide an example here>

Contributing
------------

Please see the `Contribution Guidelines`_.

Copyright
---------

This skill is provided by `Snips`_ as Open Source software. See `LICENSE.txt`_ for more
information.

.. |Build Status| image:: https://travis-ci.org/snipsco/<REPLACE ME>.svg
   :target: https://travis-ci.org/snipsco/<REPLACE ME>
   :alt: Build Status
.. |PyPI| image:: https://img.shields.io/pypi/v/<PyPi Identifier>.svg
   :target: https://pypi.python.org/pypi/<PyPi Identifier>
   :alt: PyPI
.. |MIT License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/snipsco/snips-skill-hue/master/LICENSE.txt
   :alt: MIT License

.. _`PyPI`: https://pypi.python.org/pypi/<PyPi Identifier>
.. _`pip`: http://www.pip-installer.org
.. _`Snips`: https://www.snips.ai
.. _`LICENSE.txt`: https://github.com/snipsco/snips-skill-hue/blob/master/LICENSE.txt
.. _`Contribution Guidelines`: https://github.com/snipsco/snips-skill-hue/blob/master/CONTRIBUTING.rst
.. _snipsskills: https://github.com/snipsco/snipsskills