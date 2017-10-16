# -*-: coding utf-8 -*-
""" Addon handler. """

import os

from .os_helpers import read_file
from .. import SNIPS_CACHE_DIR

class Addons:

    SPOTIFY_ENV_KEY = 'spotify_refresh_token'

    @staticmethod
    def install(addon_id, params):
        if addon_id == "spotify" and len(params) > 0:
            EnvCache.set_env(Addons.SPOTIFY_ENV_KEY, params[0])

    @staticmethod
    def update_params(params, addon_id):
        if addon_id == "spotify":
            value = EnvCache.get_env(Addons.SPOTIFY_ENV_KEY)
            if value is not None:
                params[Addons.SPOTIFY_ENV_KEY] = value
                return True
            return False
        return False

class EnvCache:

    STORE_FILE = os.path.join(SNIPS_CACHE_DIR, "env_cache")

    @staticmethod
    def get_env(key):
        cache = read_file(EnvCache.STORE_FILE)
        if cache is None:
            return None
        for line in cache.splitlines():
            if line.startswith(key + "="):
                return "=".join(line.split("=")[1:])
        return None

    @staticmethod
    def remove_env(key):
        cache = read_file(EnvCache.STORE_FILE)
        if cache is None:
            return
        filtered = []
        for line in cache.splitlines():
            if not line.startswith(key + "="):
                filtered.append(line)
        cache = "\n".join(filtered)
        EnvCache.save(cache)

    @staticmethod
    def set_env(key, value):
        EnvCache.remove_env(key)
        line = key + "=" + value + "\n"
        cache = read_file(EnvCache.STORE_FILE)
        if cache is None:
            cache = ""
        cache = cache + line
        EnvCache.save(cache)

    @staticmethod
    def save(cache):
        with open(EnvCache.STORE_FILE, "w") as f:
            f.write(cache)
