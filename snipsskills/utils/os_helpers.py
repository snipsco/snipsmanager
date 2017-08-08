# -*-: coding utf-8 -*-
""" Helper methods for OS related tasks. """

import os
import shlex
import subprocess
import urllib2

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

def remove_file(file_path):
    """ Delete a file.

    :param file_path: the path to the file.
    """
    try:
        os.remove(file_path)
    except OSError:
        pass

def download_file(url, output_file):
    """ Download a file.

    :param url: the remote location of the file.
    :param output_file: the file to write to.
    """
    downloaded_file = urllib2.urlopen(url)
    with open(output_file, 'wb') as output:
        output.write(downloaded_file.read())
