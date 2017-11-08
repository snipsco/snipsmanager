# -*-: coding utf-8 -*-

from ..base import Base
from snipsmanagercore import pretty_printer as pp
from ...utils.os_helpers import write_text_file, read_file, file_exists, ask_for_input, ask_for_password
from ...utils.cache import Cache
from ...utils.auth import Auth

# pylint: disable=too-few-public-methods
class Logout(Base):

    def run(self):
        if Cache.get_login_token() is not None:
            Logout.logout()
            pp.psuccess("You are now signed out")
        else:
            pp.psuccess("You are already signed out")

    @staticmethod
    def logout():
        Cache.clear_login_token()
