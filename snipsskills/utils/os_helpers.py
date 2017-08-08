# -*-: coding utf-8 -*-
""" Helper methods for OS related tasks. """

import os
import shlex
import subprocess

def cmd_exists(cmd):
    """ Check if a command exists.

    :param cmd: the command to look for.
    :return: true if the command exists, false otherwise.
    """
    return subprocess.call("type " + cmd, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def is_raspi_os():
    """ Check if the current system is Raspberry.

    :return: true if the current system is Raspberry.
    """
    return 'arm' in " ".join(os.uname())

def execute_command(command):
    """ Execute a shell command.

    :param command: the command to execute.
    """
    subprocess.Popen(command.split(), stdout=subprocess.PIPE).communicate()

def pipe_commands(first_command, second_command, silent):
    """ Execute piped commands: `first_command | second_command`.

    :param first_command: the first command to execute.
    :param second_command: the second command to execute.
    """
    process1 = subprocess.Popen(first_command.split(), stdout=subprocess.PIPE)
    if silent:
        FNULL = open(os.devnull, 'w')
        process2 = subprocess.Popen(second_command.split(), stdin=process1.stdout, stdout=FNULL)
    else:
        process2 = subprocess.Popen(second_command.split(), stdin=process1.stdout)
    process1.stdout.close()
    process2.communicate()
