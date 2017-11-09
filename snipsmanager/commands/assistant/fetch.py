# -*-: coding utf-8 -*-

import hashlib
import os
import shutil
import time

from ..base import Base
from ..session.login import Login
from ..session.logout import Logout
from ...utils.http_helpers import fetch_url
from ...utils.os_helpers import write_binary_file, file_exists
from ...utils.cache import Cache
from ...utils.snipsfile import Snipsfile

from ... import SNIPS_CACHE_DIR, DEFAULT_SNIPSFILE_PATH

from snipsmanagercore import pretty_printer as pp

class AssistantFetcherException(Exception):
    pass

# pylint: disable=too-few-public-methods
class AssistantFetcher(Base):

    SNIPS_TEMP_ASSISTANT_FILENAME = "assistant.zip"
    SNIPS_TEMP_ASSISTANT_PATH = os.path.join(SNIPS_CACHE_DIR, SNIPS_TEMP_ASSISTANT_FILENAME)
    CONSOLE_ASSISTANT_URL = "https://external-gateway.snips.ai/v1/assistant/{}/download"
    # CONSOLE_ASSISTANT_URL = "https://console.snips.ai/api/assistants/{}/download"


    def run(self):
        """ Command runner.

        Docopt command:
        
        snipsmanager fetch assistant [--id=<id> --url=<url> --file=<filename>]
        """
        force_download = self.options['--force-download']
        try:
            aid = self.options['--id']
            url = self.options['--url']
            file = self.options['--file']
            email = self.options['--email']
            password = self.options['--password']
            if aid is not None or url is not None or file is not None:
                AssistantFetcher.fetch_from_params(aid=aid, url=url, file=file, email=email, password=password, force_download=force_download)
            else:
                AssistantFetcher.fetch(self.options['--snipsfile'], email=email, password=password, force_download=force_download)
        except Exception as e:
            pp.perror(str(e))


    @staticmethod
    def fetch(snipsfile_path=None, email=None, password=None, force_download=False):
        if snipsfile_path is None:
            snipsfile_path = DEFAULT_SNIPSFILE_PATH
        if snipsfile_path is not None and not file_exists(snipsfile_path):
            raise AssistantFetcherException("Error fetching assistant: Snipsfile not found")
        snipsfile = Snipsfile(snipsfile_path)
        AssistantFetcher.fetch_from_snipsfile(snipsfile, email=email, password=password, force_download=force_download)


    @staticmethod
    def fetch_from_snipsfile(snipsfile, email=None, password=None, force_download=False):
        if snipsfile is None:
            raise AssistantFetcherException("Error fetching assistant: Snipsfile not found")
        AssistantFetcher.fetch_from_params(aid=snipsfile.assistant_id, url=snipsfile.assistant_url, file=snipsfile.assistant_file, email=email, password=password, force_download=force_download)


    @staticmethod
    def fetch_from_params(aid=None, url=None, file=None, email=None, password=None, force_download=False):
        pp.pcommand("Fetching assistant")

        if aid is None and url is None and file is None:
            raise AssistantFetcherException("Error fetching assistant. Please provide an assistant ID, a public URL, or a filename")

        if url:
            AssistantFetcher.download_public_assistant(url, force_download=force_download)
        elif aid:
            AssistantFetcher.download_console_assistant(aid, email=email, password=password, force_download=force_download)
        elif file:
            AssistantFetcher.copy_local_file(file)


    @staticmethod
    def download_public_assistant(url, force_download=False):
        message = pp.ConsoleMessage("Downloading assistant from {}".format(url))
        message.start()

        if not force_download and AssistantFetcher.exists_cached_from_url(url):
            message.done()
            pp.psubsuccess("Using cached version from {}".format(SNIPS_CACHE_DIR))
            AssistantFetcher.copy_to_temp_assistant_from_url(url)
            return

        try:
            content = fetch_url(url)
            message.done()
        except:
            raise AssistantFetcherException("Error downloading assistant. Please make sure the assistant URL is correct")

        filepath = AssistantFetcher.get_assistant_cache_path_from_url(url)
        message = pp.ConsoleMessage("Saving assistant to {}".format(SNIPS_CACHE_DIR))
        message.start()
        write_binary_file(filepath, content)
        message.done()
        AssistantFetcher.copy_to_temp_assistant_from_url(url)


    @staticmethod
    def download_console_assistant(aid, email=None, password=None, force_download=False):
        start_message = "Fetching assistant $GREEN{}$RESET from the Snips Console".format(aid)

        if not force_download and AssistantFetcher.exists_cached_from_assistant_id(aid):
            pp.psubsuccess(start_message)
            pp.psubsuccess("Using cached version: {}".format(AssistantFetcher.get_assistant_cache_path_from_assistant_id(aid)))
            AssistantFetcher.copy_to_temp_assistant_from_assistant_id(aid)
            return

        token = Cache.get_login_token()
        if token is None:
            token = AssistantFetcher.get_token(email=email, password=password)

        message = pp.ConsoleMessage(start_message)
        message.start()
        try:
            content = AssistantFetcher.download_console_assistant_only(aid, token)
            message.done()
        except Exception as e:
            message.error()
            Logout.logout()
            token = AssistantFetcher.get_token(email=email, password=password)
            message = pp.ConsoleMessage("Retrying to fetch assistant $GREEN{}$RESET from the Snips Console".format(aid))
            message.start()
            try:
                content = AssistantFetcher.download_console_assistant_only(aid, token)
                message.done()
            except Exception:
                message.error()
                raise AssistantFetcherException("Error fetching assistant from the console. Please make sure the ID is correct, and that you are signed in")

        filepath = AssistantFetcher.get_assistant_cache_path_from_assistant_id(aid)
        message = pp.ConsoleMessage("Saving assistant to {}".format(filepath))
        message.start()
        write_binary_file(filepath, content)
        message.done()
        AssistantFetcher.copy_to_temp_assistant_from_assistant_id(aid)


    @staticmethod
    def download_console_assistant_only(aid, token):
        url = AssistantFetcher.CONSOLE_ASSISTANT_URL.format(aid)
        return fetch_url(url, headers={'Authorization': token, 'Accept': 'application/json'})


    @staticmethod
    def exists_cached_from_url(url):
        return file_exists(AssistantFetcher.get_assistant_cache_path_from_url(url))


    @staticmethod
    def exists_cached_from_assistant_id(assistant_id):
        return file_exists(AssistantFetcher.get_assistant_cache_path_from_assistant_id(assistant_id))


    @staticmethod
    def exists_assistant_filename(filename):
        return file_exists(AssistantFetcher.get_assistant_file_path(filename))


    @staticmethod
    def get_assistant_filename_from_url(url):
        return "assistant_" + hashlib.sha224(url).hexdigest() + ".zip"


    @staticmethod
    def get_assistant_filename_from_assistant_id(assistant_id):
        return "assistant_{}.zip".format(assistant_id)


    @staticmethod
    def get_assistant_cache_path_from_url(url):
        return AssistantFetcher.get_assistant_file_path(AssistantFetcher.get_assistant_filename_from_url(url))


    @staticmethod
    def get_assistant_cache_path_from_assistant_id(assistant_id):
        return AssistantFetcher.get_assistant_file_path(AssistantFetcher.get_assistant_filename_from_assistant_id(assistant_id))


    @staticmethod
    def get_assistant_file_path(filename):
        return os.path.join(SNIPS_CACHE_DIR, filename)


    @staticmethod
    def get_token(email=None, password=None):
        try:
            return Login.login(email=email, password=password, greeting="Please enter your Snips Console credentials to download your assistant.", silent=True)
        except Exception as e:
            raise AssistantFetcherException("Error logging in: {}".format(str(e)))


    @staticmethod
    def copy_to_temp_assistant_from_url(url):
        AssistantFetcher.copy_local_file(AssistantFetcher.get_assistant_cache_path_from_url(url), silent=True)
    

    @staticmethod
    def copy_to_temp_assistant_from_assistant_id(assistant_id):
        AssistantFetcher.copy_local_file(AssistantFetcher.get_assistant_cache_path_from_assistant_id(assistant_id), silent=True)


    @staticmethod
    def copy_local_file(file_path, silent=False):
        if not silent:
            message = pp.ConsoleMessage("Copying assistant {} to {}".format(file_path, AssistantFetcher.SNIPS_TEMP_ASSISTANT_PATH))
            message.start()
        
        error = None
        if not file_exists(file_path):
            error = "Error: failed to locate file {}".format(file_path)
        else:
            try:
                shutil.copy2(file_path, AssistantFetcher.SNIPS_TEMP_ASSISTANT_PATH)
            except Exception as e:
                error = "Error: failed to copy file {}. Make sure you have write permissions to {}".format(file_path, AssistantFetcher.SNIPS_TEMP_ASSISTANT_PATH)

        if error is not None:
            if not silent:
                message.error()
            raise AssistantFetcherException(error)
        else:
            if not silent:
                message.done()
