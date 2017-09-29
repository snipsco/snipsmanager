# -*-: coding utf-8 -*-

from ..base import Base
from snipsskillscore import pretty_printer as pp
from ...utils.os_helpers import write_text_file, read_file, file_exists, ask_for_input, ask_for_password
from ...utils.cache import Cache
from ...utils.auth import Auth


class InvalidTokenException(Exception):
    pass


class Login(Base):

    def run(self):
        try:
            Login.login()
        except Exception as e:
            pp.perror("Error logging in: {}".format(str(e)))


    @staticmethod
    def login(greeting=None, silent=False):
        token = Cache.get_login_token()
        if not token:
            pp.pcommand(greeting or "Please enter your Snips Console credentials")
            email = ask_for_input("Email address:")
            password = ask_for_password("Password:")
            token = Auth.retrieve_token(email, password)
            if token is not None:
                Cache.save_login_token(token)
                pp.psuccess("You are now signed in")
            else:
                raise InvalidTokenException("Could not validate authentication token")
        else:
            if not silent:
                pp.psuccess("You are already signed in")
        return token
