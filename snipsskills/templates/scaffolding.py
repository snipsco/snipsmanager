README_TEMPLATE = '' \
'{} skill for Snips\n' \
'======================================\n' \
'\n' \
'|Build Status| |PyPI| |MIT License|\n' \
'\n' \
'<Skill description> \n' \
'\n' \
'Installation\n' \
'------------\n' \
'\n' \
'The skill is on `PyPI`_, so you can just install it with `pip`_:\n' \
'\n' \
'.. code-block:: console\n' \
'\n' \
    '$ pip install <skill pypi name>\n' \
'\n' \
'Usage\n' \
'-----\n' \
'\n' \
'\n' \
'Pull Request checklist\n' \
'----------------------\n' \
'\n' \
'To ensure high quality code, before opening a pull request : make sure that you wrote tests for your code, and that you linted your code.\n' \
'Before opening the pull request, run your unit tests with ``python setup.py test`` and lint your code with ``python setup.py lint --lint-rcfile lint.cfg`` \n' \
'\n' \
'\n' \
'Copyright\n' \
'---------\n' \
'\n' \
'This skill is provided by `Snips`_ as Open Source software. See `LICENSE.txt`_ for more\n' \
'information.\n' \
'\n' \
'.. |Build Status| image:: https://travis-ci.org/snipsco/<skill travis badge>.svg\n' \
   ':target: https://travis-ci.org/snipsco/\n' \
   ':alt: Build Status\n' \
'.. |PyPI| image::\n' \
   ':target:\n' \
   ':alt: PyPI\n' \
'.. |MIT License| image:: https://img.shields.io/badge/license-MIT-blue.svg\n' \
   ':target: https://raw.githubusercontent.com/snipsco/snips-skill-hue/master/LICENSE.txt\n' \
   ':alt: MIT License\n' \
'\n' \
'.. _`PyPI`:\n' \
'.. _`pip`: http://www.pip-installer.org\n' \
'.. _`Snips`: https://www.snips.ai\n' \
'\n' \
'.. _`LICENSE.txt`: https://github.com/snipsco/snips-skill-hue/blob/master/LICENSE.txt\n' \
'.. _snipsskills: https://github.com/snipsco/snipsskills\n'


SETUP_TEMPLATE = "" \
"from setuptools import setup \n" \
" \n" \
"setup( \n" \
"    name='{}', \n" \
"    version='0.0.0.1', \n" \
"    description='{} skill for Snips', \n" \
"    author='<Author>', \n" \
"    author_email='<Author email>', \n" \
"    url='<Github repository>', \n" \
"    download_url='', \n" \
"    license='MIT', \n" \
"    install_requires=[], \n" \
"    setup_requires=['green'], \n" \
"    keywords=['snips'], \n" \
"    include_package_data=True, \n" \
"    packages=[ \n" \
"        '{}' \n" \
"    ] \n" \
") \n"

LICENSE_TEMPLATE = ""\
"MIT License \n" \
" \n" \
"Copyright (c) 2017 Snips \n" \
" \n" \
"Permission is hereby granted, free of charge, to any person obtaining a copy \n" \
"of this software and associated documentation files (the \"Software\"), to deal \n" \
"in the Software without restriction, including without limitation the rights \n" \
"to use, copy, modify, merge, publish, distribute, sublicense, and/or sell \n" \
"copies of the Software, and to permit persons to whom the Software is \n" \
"furnished to do so, subject to the following conditions: \n" \
" \n" \
"The above copyright notice and this permission notice shall be included in all \n" \
"copies or substantial portions of the Software. \n" \
" \n" \
"THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR \n" \
"IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, \n" \
"FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE \n" \
"AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER \n" \
"LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, \n" \
"OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE \n" \
"SOFTWARE. \n" \

MANIFEST_TEMPLATE = ""\
"include LICENSE.txt\n" \
"include {}/Snipsspec"

LINT_TEMPLATE = ""\
"[MESSAGES CONTROL]\n" \
"disable=too-few-public-methods"

SETUP_CONFIG_TEMPLATE = ""\
"[bdist_wheel]\n" \
"universal=1"