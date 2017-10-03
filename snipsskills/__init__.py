# -*-: coding utf-8 -*-
""" snipsskills module """
__version__ = '0.1.6.16'

import os
import logging

SNIPS_CACHE_DIR_NAME = ".snips"
HOME_DIR = os.path.expanduser("~")
SNIPS_CACHE_DIR = os.path.join(HOME_DIR, SNIPS_CACHE_DIR_NAME)
NODE_MODULES_LOCATION = SNIPS_CACHE_DIR
NODE_MODULES_PATH = os.path.join(NODE_MODULES_LOCATION, "node_modules")
DEFAULT_SNIPSFILE_PATH = os.path.join(os.getcwd(), "Snipsfile")
SNIPS_CACHE_INTENTS_DIR = os.path.join(SNIPS_CACHE_DIR, "intents")
SNIPS_CACHE_INTENT_REGISTRY_FILE = os.path.join(SNIPS_CACHE_INTENTS_DIR, "intent_registry.py")

ASOUNDRC_DEST_PATH = os.path.join(HOME_DIR, ".asoundrc")
ASOUNDCONF_DEST_PATH = "/etc/asound.conf"


def prepare_cache():
    if not os.path.exists(SNIPS_CACHE_DIR):
        os.makedirs(SNIPS_CACHE_DIR)

prepare_cache()

logger = logging.getLogger()
handler = logging.StreamHandler()
log_format = '\033[2m%(asctime)s\033[0m [%(levelname)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(log_format, date_format)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

RESET_SEQ = u'\033[0m'
GREEN_COLOR = u'\033[32m'
BLUE_COLOR = u'\033[34m'
