# -*-: coding utf-8 -*-
""" Bluetooth setup utilities. """

import getpass
import os
import subprocess
import time

from snipsskillscore.logging import log, log_warning

from .os_helpers import cmd_exists, download_file, execute_command, remove_file, ask_yes_no, which
from .systemd import Systemd

SNIPSBLE_SERVICE_NAME = "snipsble"

# DO NOT CHANGE
SNIPS_BLE_SERVICE_UUID = "13EA4259-9D9E-42D1-A78B-638ED22CC768"
SNIPS_BLE_CHARACTERISTIC_UUID = "81D97A06-7A2D-4A98-A2E2-41688E3D8283"


class Bluetooth:
    """ Bluetooth setup utilities. """

    @staticmethod
    def setup(mqtt_hostname, mqtt_port):
        """ Setting up Bluetooth Relay MQTT service. """
        if ask_yes_no("Would you like to enable Bluetooth for this device?") == False:
            return

        try:
            Bluetooth.install_node()
        except Exception:
            log_warning("Could not download Node, which is required for Bluetooth. " +
                        "Please install Node manually, and restart the snipsskills installation script.")
            return

        Bluetooth.install_mqtt_relay()
        Bluetooth.setup_systemd(mqtt_hostname, mqtt_port)

    @staticmethod
    def install_node():
        """ Install node using dpkg, if it is not installed. """
        if cmd_exists('node'):
            return

        log("Node is required for Bluetooth setup. Installing Node.")

        filename = "node_latest_armhf.deb"

        log("Downloading Node.")
        download_file(
            "http://node-arm.herokuapp.com/node_latest_armhf.deb", filename)

        log("Installing Node.")
        execute_command("sudo dpkg -i node_latest_armhf.deb")
        remove_file(filename)

    @staticmethod
    def install_mqtt_relay():
        """ Install snips-mqtt-relay. """
        if not cmd_exists('node'):
            return

        log("Installing Node module: snips-mqtt-relay.")
        execute_command(
            "npm install --no-cache --prefix=./.snips snips-mqtt-relay &> /dev/null")

    @staticmethod
    def setup_systemd(mqtt_hostname, mqtt_port):
        (snipsble_path, node_path) = Bluetooth.get_params()
        contents = Systemd.get_template(SNIPSBLE_SERVICE_NAME)
        if contents is None:
            return
        contents = contents.replace("{{SNIPSBLE_PATH}}", snipsble_path) \
            .replace("{{SNIPS_BLE_SERVICE_UUID}}", SNIPS_BLE_SERVICE_UUID) \
            .replace("{{SNIPS_BLE_CHARACTERISTIC_UUID}}", SNIPS_BLE_CHARACTERISTIC_UUID) \
            .replace("{{SNIPS_MQTT_HOSTNAME}}", mqtt_hostname) \
            .replace("{{SNIPS_MQTT_PORT}}", str(mqtt_port)) \
            .replace("{{NODE_PATH}}", str(node_path))
        Systemd.write_systemd_file(SNIPSBLE_SERVICE_NAME, None, contents)
        Systemd.enable_service(None, SNIPSBLE_SERVICE_NAME)

    @staticmethod
    def get_params():
        snipsble_path = "{}/.snips/node_modules/snips-mqtt-relay".format(
            os.getcwd())
        node_path = which('node')
        return (snipsble_path, node_path)
