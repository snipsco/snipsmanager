# -*-: coding utf-8 -*-
""" Helper methods for OS related tasks. """

from getpass import getpass
import os
import platform
import re
import shlex
import subprocess
import urllib2

from snipsmanagercore import pretty_printer as pp

email_regex = r"[^@]+@[^@]+\.[^@]+"

github_url_regex = re.compile(
                   r'^(?:http|ftp|git)s?://' # http:// or https://
                   r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                   r'localhost|' #localhost...
                   r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                   r'(?::\d+)?' # optional port
                   r'(?:/?|[/?]\S+)$', re.IGNORECASE)

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


def is_mac_os():
    """ Check if the current system is OSX.

    :return: true if the current system is OSX.
    """
    return 'Darwin' in platform.system()


def is_node_available():
    return cmd_exists('node') and cmd_exists('npm')


def file_exists(file_path):
    return os.path.exists(file_path)


def create_dir(dir_name):
    """ Create directory in the current working directory, if it does
        not exist already.

    :param dir_name: the name of the directory.
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def create_dir_verbose(dir_name, indentation_level):
    create_dir(dir_name)


def write_text_file(output_file_path, text):
    with open(output_file_path, "w") as f:
        f.write(text)


def write_binary_file(output_file_path, content):
    with open(output_file_path, "wb") as f:
        f.write(content)


def read_file(file_path):
    if not file_exists(file_path):
        return None
    with open(file_path, "r") as f:
        return f.read()
    return None


def write_text_file_verbose(output_file_path, text, indentation_level):
    write_text_file(output_file_path, text)


def execute_command(command, silent=False):
    """ Execute a shell command.

    :param command: the command to execute.
    :param silent: if True, do not output anything to terminal.
    """
    if silent:
        stdout = open(os.devnull, 'w')
        stderr = open(os.devnull, 'w')
    else:
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
    return subprocess.Popen(command.split(), stdout=stdout, stderr=stderr).communicate()


def pipe_commands(first_command, second_command, silent):
    """ Execute piped commands: `first_command | second_command`.

    :param first_command: the first command to execute.
    :param second_command: the second command to execute.
    """
    process1 = subprocess.Popen(first_command.split(), stdout=subprocess.PIPE)
    if silent:
        FNULL = open(os.devnull, 'w')
        process2 = subprocess.Popen(
            second_command.split(), stdin=process1.stdout, stdout=FNULL)
    else:
        process2 = subprocess.Popen(
            second_command.split(), stdin=process1.stdout)
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


def ask_yes_no(question, default_value=None):
    """ Ask a yes/no question in the prompt.

    :param question: the question to ask.
    :return: true if the user answered yes (or empty), false otherwise
    """
    if default_value is not None:
        return default_value

    answer = raw_input("{} [Y/n] ".format(question))
    if answer is not None and answer.strip() != "" and answer.lower() != "y":
        return False
    return True


def ask_for_input(question, default_value=None):
    if default_value and len(default_value) > 0:
        question = pp.generate_user_input_string("{} [{}] ".format(question, default_value))
        answer = raw_input(question)
        if len(answer) == 0:  # The user hit enter.
            answer = default_value
    else:
        question = pp.generate_user_input_string(question)
        answer = raw_input(question)

    if answer is not None and answer.strip() != "":
        return answer
    else:
        return None


def ask_for_password(question):
    question = pp.generate_user_input_string(question)
    answer = getpass(question)
    if answer is not None and answer.strip() != "":
        return answer.strip()
    else:
        return None


def which(command):
    """ Get full path for an executable.

    :param command: the executable command, e.g. 'node'.
    :return: the full path for the command, e.g. '/usr/local/bin/node'.
    """
    try:
        return subprocess.check_output(
            ['which', command]).strip()
    except subprocess.CalledProcessError:
        return None


def reboot():
    """ Reboot the device."""
    execute_command("sudo reboot")


def get_os_name():
    os_release = subprocess.check_output(['cat', '/etc/os-release'])
    for line in os_release.splitlines():
        if line.startswith("PRETTY_NAME="):
            split = line.split("=")
            if len(split) > 1:
                os_version = split[1]
                return os_version.replace("\"", "")
    return None


def get_revision():
    process1 = subprocess.Popen('cat /proc/cpuinfo'.split(), stdout=subprocess.PIPE)
    process2 = subprocess.Popen('grep Revision'.split(), stdin=process1.stdout, stdout=subprocess.PIPE)
    process3 = subprocess.Popen(['awk', '{print $3}'], stdin=process2.stdout)
    process1.stdout.close()
    process2.stdout.close()
    return process3.communicate()


def get_sysinfo():
    return {
        "os_name": get_os_name()
    }


def get_command_output(command_array):
    return subprocess.check_output(command_array)


def get_user_email_git():
    if cmd_exists("git"):
        command = "git config user.email"
        output = get_command_output(command.split())
        if output is not None and len(output) > 0:
            return output.strip()
        return None
    else:
        return None


def email_is_valid(email):
    return True if re.match(email_regex, email) else False


def is_valid_github_url(url):
    return True if re.match(github_url_regex, url) else False
