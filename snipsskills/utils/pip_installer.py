# -*-: coding utf-8 -*-
""" pip module installer. """

import pip

# pylint: disable=too-few-public-methods
class PipInstaller:
    """ pip module installer. """

    @staticmethod
    def install(module):
        """ Install a pip module.

        :param module: the pip module name or URL.
        """
        pip.main(['install', '--quiet', module])
