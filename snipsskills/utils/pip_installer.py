# -*-: coding utf-8 -*-
""" pip module installer. """

import pip

# pylint: disable=too-few-public-methods
class PipInstaller:
    """ pip module installer. """

    @staticmethod
    def install(url):
        """ Install a pip module.

        :param module: the pip module name or URL.
        """
        if url.startswith("https://"):
            url = "git+" + url
        pip.main(['install', '--quiet', url])
