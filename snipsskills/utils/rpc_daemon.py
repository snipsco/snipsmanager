# -*-: coding utf-8 -*-
""" Snips Daemon for controlling Snips. """

import json
import time

from socket import error as socket_error

import paho.mqtt.client as mqtt

from snipsskillscore.logging import debug_log, LOGGING_ENABLED
from snipsskillscore.thread_handler import ThreadHandler

from .os_helpers import reboot, get_sysinfo

class RPCDaemon():
    """ Snips Daemon for controlling Snips. """

    def __init__(self,
                 logging_enabled):
        """ Initialisation.

        """
        self.thread_handler = ThreadHandler()

        LOGGING_ENABLED = logging_enabled

    def start(self):
        """ Start the MQTT client. """
        self.thread_handler.run(target=self.start_blocking)
        self.thread_handler.start_run_loop()

    def start_blocking(self, run_event):
        """ Start the BLE client, as a blocking method.

        :param run_event: a run event object provided by the thread handler.
        """
        pass

    # pylint: disable=unused-argument
    def on_message(self, client, userdata, msg):
        """ Callback when the BLE client received a new message.

        :param client: the BLE client.
        :param userdata: unused.
        :param msg: the BLE message.
        """
        if msg.topic == "daemon/reboot":
            self.handle_reboot()
        elif msg.topic == "daemon/ask_sysinfo":
            self.handle_ask_sysinfo()
        	# self.handle_reboot()
            # payload = json.loads(msg.payload.decode('utf-8'))
            # intent = IntentParser.parse(payload, self.registry.intent_classes)
            # debug_log("New intent: {}".format(str(intent.intentName)))
            # if self.handle_intent:
            #     self.handle_intent(intent)

    def publish(self, topic, message):
        """ Publish a message to BLE.

        :param topic: the topic on which to publish the message.
        :param message: the message to publish.
        """
        pass

    def handle_reboot(self):
        """ Handle a reboot message."""
        reboot()

    def handle_ask_sysinfo(self):
        """ Handle an ask_sysinfo message."""

        self.publish("daemon/reply_sysinfo", get_sysinfo())

    def handle_write_snipsfile(self, snipsfile):
        """ Handle a write_snipsfile message."""
        pass

    def handle_install(self):
        """ Handle a snipsskills install message."""
        pass