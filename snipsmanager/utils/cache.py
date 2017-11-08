# -*-: coding utf-8 -*-
""" Simple caching. """

import os
from .os_helpers import write_text_file, read_file, create_dir, remove_file

from .. import SNIPS_CACHE_DIR

class Cache:

    STORE_FILE = os.path.join(SNIPS_CACHE_DIR, "token_store")

    @staticmethod
    def get_login_token():
        return read_file(Cache.STORE_FILE)

    @staticmethod
    def save_login_token(token):
        write_text_file(Cache.STORE_FILE, token)
    
    @staticmethod
    def clear_login_token():
        remove_file(Cache.STORE_FILE)