# -*-: coding utf-8 -*-
""" snipsskills module """
__version__ = '0.1.6.13'

from .utils.os_helpers import create_dir

SNIPS_CACHE_DIR = ".snips"

def prepare_cache():
	create_dir(SNIPS_CACHE_DIR)