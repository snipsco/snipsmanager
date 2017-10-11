# -*-: coding utf-8 -*-
""" snipsskills module """
__version__ = '0.1.6.21'

import os
import logging

HOME_DIR = os.path.expanduser('~')
if 'arm' in " ".join(os.uname()):
    HOME_DIR = "/home/pi"

SNIPS_CACHE_DIR_NAME = ".snips"
SNIPS_CACHE_DIR = os.path.join(HOME_DIR, SNIPS_CACHE_DIR_NAME)
NODE_MODULES_LOCATION = SNIPS_CACHE_DIR
NODE_MODULES_PATH = os.path.join(NODE_MODULES_LOCATION, "node_modules")
DEFAULT_SNIPSFILE_PATH = os.path.join(os.getcwd(), "Snipsfile")
SNIPS_CACHE_INTENTS_DIR = os.path.join(SNIPS_CACHE_DIR, "intents")
SNIPS_CACHE_INTENT_REGISTRY_FILE = os.path.join(SNIPS_CACHE_INTENTS_DIR, "intent_registry.py")

DEB_VENV = "/opt/venvs/snipsskills"
SHELL_COMMAND = "/bin/bash"
PIP_BINARY = os.path.join(DEB_VENV, "bin/pip")

ASOUNDRC_DEST_PATH = os.path.join(HOME_DIR, ".asoundrc")
ASOUNDCONF_DEST_PATH = "/etc/asound.conf"

def prepare_cache():
    if not os.path.exists(HOME_DIR):
        os.makedirs(HOME_DIR)
    if not os.path.exists(SNIPS_CACHE_DIR):
        os.makedirs(SNIPS_CACHE_DIR)

prepare_cache()

logger = logging.getLogger(__name__)
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
