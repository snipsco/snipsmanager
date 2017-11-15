# -*-: coding utf-8 -*-

import os

from ..base import Base
from ...utils.os_helpers import is_raspi_os, is_node_available, execute_command, download_file, file_exists

from ... import prepare_cache, NODE_MODULES_PARENT_DIR, NODE_MODULES_DIR

from snipsmanagercore import pretty_printer as pp

class BluetoothInstallerException(Exception):
    pass


class BluetoothInstaller(Base):
    
    SNIPS_MQTT_RELAY_MODULE_NAME = "snips-mqtt-relay"

    def run(self):
        try:
            BluetoothInstaller.install(force_download=self.options['--force-download'])
        except Exception as e:
            pp.perror(str(e))


    @staticmethod
    def install(force_download=False):
        pp.pcommand("Setting up Bluetooth")

        if not is_raspi_os():
            raise BluetoothInstallerException("Error: Bluetooth is only available on Raspberry Pi")

        if not is_node_available():
            BluetoothInstaller.install_node()
        
        if force_download or not BluetoothInstaller.is_snips_mqtt_relay_installed():
            message = pp.ConsoleMessage("Installing Node module $GREEN{}$RESET".format(BluetoothInstaller.SNIPS_MQTT_RELAY_MODULE_NAME))
            message.start()
            try:
                execute_command("sudo npm install --no-cache --prefix={} {}".format(NODE_MODULES_PARENT_DIR, BluetoothInstaller.SNIPS_MQTT_RELAY_MODULE_NAME), True)
                message.done()
            except:
                message.error()
                raise BluetoothInstallerException("Error: Error installing Bluetooth module {}. Please install it manually".format(BluetoothInstaller.SNIPS_MQTT_RELAY_MODULE_NAME))

        pp.psuccess("Bluetooth is successfully installed")


    @staticmethod
    def is_snips_mqtt_relay_installed():
        return os.path.isdir(os.path.join(NODE_MODULES_DIR, BluetoothInstaller.SNIPS_MQTT_RELAY_MODULE_NAME))
        

    @staticmethod
    def install_node():
        pp.psubmessage("Node is not available. Installing node.", indent=True)
        message = pp.ConsoleMessage("Removing previous version of Node")
        message.start()
        try:
            execute_command("sudo apt-get -y remove nodejs nodejs-legacy npm")
            message.done()
        except:
            message.error()
            pass


        deb_file = "node_latest_armhf.deb"
        deb_url = "http://node-arm.herokuapp.com/node_latest_armhf.deb"
        
        message = pp.ConsoleMessage("Downloading Raspbian-compatible version of Node")
        message.start()

        try:
            download_file(deb_url, deb_file)
            message.done()
        except:
            message.error()
            raise BluetoothInstallerException("Error: failed to download compatible version of Node")


        message = pp.ConsoleMessage("Installing Node")
        message.start()
        try:
            execute_command("sudo dpkg -i {}".format(deb_file))
            message.done()
        except:
            message.error()
            raise BluetoothInstallerException("Error: installing Node. Please install Node manually")

        try:
            remove_file(filename)
        except:
            pass

        pp.psuccess("Successfully installed Node")
