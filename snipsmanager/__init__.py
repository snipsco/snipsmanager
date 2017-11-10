# -*-: coding utf-8 -*-
""" snipsmanager module """
__version__ = '0.1.6.32'

import os
import logging
import subprocess
import sys

def which(command, default_value):
    try:
        return subprocess.check_output(["which", command]).strip()
    except subprocess.CalledProcessError:
        return default_value

HOME_DIR = os.path.expanduser('~')
if 'arm' in " ".join(os.uname()):
    HOME_DIR = "/home/pi"

PACKAGE_NAME = "snipsmanager"
SNIPS_CACHE_DIR_NAME = ".snips"
SNIPS_CACHE_DIR = os.path.join(HOME_DIR, SNIPS_CACHE_DIR_NAME)
NODE_MODULES_PARENT_DIR = SNIPS_CACHE_DIR
NODE_MODULES_DIR = os.path.join(NODE_MODULES_PARENT_DIR, "node_modules")
DEFAULT_SNIPSFILE_PATH = os.path.join(os.getcwd(), "Snipsfile")
SNIPS_CACHE_INTENTS_DIR = os.path.join(SNIPS_CACHE_DIR, "intents")
SNIPS_CACHE_INTENT_REGISTRY_FILE = os.path.join(SNIPS_CACHE_INTENTS_DIR, "intent_registry.py")
ASOUNDRC_DEST_PATH = os.path.join(HOME_DIR, ".asoundrc")
ASOUNDCONF_DEST_PATH = "/etc/asound.conf"

SHELL_COMMAND = which("bash", "/bin/bash")

this_dir, this_filename = os.path.split(__file__)
__DEB_VENV = "/opt/venvs/{}".format(PACKAGE_NAME)
if this_dir.startswith(__DEB_VENV):
    # We need to force this in Deb version
    VENV_PATH = __DEB_VENV
    PIP_BINARY = os.path.join(VENV_PATH, "bin/pip")
elif 'VIRTUAL_ENV' in os.environ:
    VENV_PATH = os.environ['VIRTUAL_ENV']
    PIP_BINARY = os.path.join(VENV_PATH, "bin/pip")
else:
    VENV_PATH = None
    PIP_BINARY = which("pip", "/usr/local/bin/pip")

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
