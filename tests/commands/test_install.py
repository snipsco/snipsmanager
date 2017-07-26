"""Tests for the `snipsskills install` command."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestHello(TestCase):

    def test_returns_multiple_lines(self):
        output = popen(['snipsskills', 'install'], stdout=PIPE).communicate()[0]
        self.assertTrue('Found' in output)
