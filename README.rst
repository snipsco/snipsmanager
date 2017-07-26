Snips Skills Manager
====================

|Build Status| |PyPI| |MIT License|


Installation
------------

The skill is on `PyPI`_, so you can just install it with `pip`_:

.. code-block:: console

    $ pip install snipslocalmusic

Usage
-----

The skill allows you to play music using local files.

.. code-block:: python

    from snipslocalmusic.snipslocalmusic import SnipsLocalMusic

    music = SnipsLocalMusic("db.json") 
    music.play(None, None, None, "Bach")

Copyright
---------

This skill is provided by `Snips`_ as Open Source software. See `LICENSE.txt`_ for more
information.

.. |Build Status| image:: https://travis-ci.org/snipsco/snips-skill-localmusic.svg
   :target: https://travis-ci.org/snipsco/snips-skill-localmusic
   :alt: Build Status
.. |PyPI| image:: https://img.shields.io/pypi/v/snipslocalmusic.svg
   :target: https://pypi.python.org/pypi/snipslocalmusic
   :alt: PyPI
.. |MIT License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/snipsco/snips-skill-localmusic/master/LICENSE.txt
   :alt: MIT License

.. _`PyPI`: https://pypi.python.org/pypi/snipshue
.. _`pip`: http://www.pip-installer.org
.. _`Snips`: https://www.snips.ai
.. _`LICENSE.txt`: https://github.com/snipsco/snips-skill-smartercoffee/blob/master/LICENSE.txt











Snips Skills Manager
====================

*A skeleton command line program in Python.*


Purpose
-------

This is a skeleton application which demonstrates how to properly structure a
Python CLI application.

I've done my best to structure this in a way that makes sense for *most* users,
but if you have any feedback, please open a Github issue and I'll take a look.

The idea with this project is that you should be able to use this as a template
for building new CLI apps.

You can fork this project and customize it to your liking, or just use it as a
reference.


Usage
-----

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

    $ pip install -e .[test]

If you'd like to run all tests for this project (*assuming you've written
some*), you would run the following command::

    $ python setup.py test

This will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.

Lastly, if you'd like to cut a new release of this CLI tool, and publish it to
the Python Package Index (`PyPI <https://pypi.python.org/pypi>`_), you can do so
by running::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*

This will build both a source tarball of your CLI tool, as well as a newer wheel
build (*and this will, by default, run on all platforms*).

The ``twine upload`` command (which requires you to install the `twine
<https://pypi.python.org/pypi/twine>`_ tool) will then securely upload your
new package to PyPI so everyone in the world can use it!
