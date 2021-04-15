import sys
import unittest
from io import StringIO


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout, sys.stdout = sys.stdout, StringIO()
        self.stderr, sys.stderr = sys.stderr, StringIO()

    def assertStdOut(self, value):
        self.assertEqual(sys.stdout.getvalue().strip(), value.strip())

    def assertStdErr(self, value):
        self.assertEqual(sys.stderr.getvalue().strip(), value.strip())


class PseudoTTY(object):
    """Pseudo TTY wrapper around stdin."""

    def __init__(self, underlying):
        self.__underlying = underlying

    def __getattr__(self, name):
        return getattr(self.__underlying, name)

    def isatty(self):
        return True
