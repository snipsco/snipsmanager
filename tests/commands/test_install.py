"""Tests for the `snipsskills install` command."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestHello(TestCase):

    def test_returns_multiple_lines(self):
        self.assertTrue(True)
