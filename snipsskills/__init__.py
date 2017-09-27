# -*-: coding utf-8 -*-
""" snipsskills module """
__version__ = '0.1.6.13'

import os

from .utils.os_helpers import create_dir

SNIPS_CACHE_DIR_NAME = ".snips"
HOME_DIR = os.path.expanduser("~")
SNIPS_CACHE_DIR = os.path.join(HOME_DIR, SNIPS_CACHE_DIR_NAME)
NODE_MODULES_LOCATION = SNIPS_CACHE_DIR
NODE_MODULES_PATH = os.path.join(NODE_MODULES_LOCATION, "node_modules")

def prepare_cache():
	create_dir(SNIPS_CACHE_DIR)