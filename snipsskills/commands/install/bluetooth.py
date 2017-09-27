# -*-: coding utf-8 -*-

import os

from ..base import Base
from ...utils.bluetooth import Bluetooth
from ...utils.os_helpers import is_raspi_os, is_node_available, execute_command, download_file

from snipsskills import prepare_cache, NODE_MODULES_LOCATION

from snipsskillscore import pretty_printer as pp

class BluetoothInstallerException(Exception):
    pass


class BluetoothInstaller(Base):
    
    def run(self):
        try:
            BluetoothInstaller.install()
        except Exception as e:
            pp.perror(str(e))


    @staticmethod
    def install():
        pp.pcommand("Setting up Bluetooth.")

        if not is_raspi_os():
            raise BluetoothInstallerException("Error: Bluetooth is only available on a Raspberry Pi.")

        if not is_node_available():
            BluetoothInstaller.install_node()

        node_module = "snips-mqtt-relay"
        
        message = pp.ConsoleMessage("Installing Node module $GREEN{}$RESET.".format(node_module))
        message.start()
        
        prepare_cache()
        try:
            execute_command("npm install --no-cache --prefix={} {}".format(NODE_MODULES_LOCATION, node_module), True)
            message.done()
        except:
            message.error()
            raise BluetoothInstallerException("Error: Error installing Bluetooth module {}. Please install it manually.".format(node_module))

        pp.psuccess("Bluetooth is successfully installed.")


    @staticmethod
    def install_node():
        pp.psubmessage("Node is not available. Installing node.", indent=True)
        message = pp.ConsoleMessage("Removing previous version of Node.")
        message.start()
        try:
            execute_command("sudo apt-get -y remove nodejs nodejs-legacy npm")
            message.done()
        except:
            message.error()
            pass


        deb_file = "node_latest_armhf.deb"
        deb_url = "http://node-arm.herokuapp.com/node_latest_armhf.deb"
        
        message = pp.ConsoleMessage("Downloading Raspbian-compatible version of Node.")
        message.start()

        try:
            download_file(deb_url, deb_file)
            message.done()
        except:
            message.error()
            raise BluetoothInstallerException("Error: failed to download compatible version of Node.")


        message = pp.ConsoleMessage("Installing Node.")
        message.start()
        try:
            execute_command("sudo dpkg -i {}".format(deb_file))
            message.done()
        except:
            message.error()
            raise BluetoothInstallerException("Error: installing Node. Please install Node manually.")

        try:
            remove_file(filename)
        except:
            pass

        pp.psuccess("Successfully installed Node.")
