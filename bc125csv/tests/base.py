import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    # Python 2
    from StringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO

try:
    from unittest import mock
except ImportError:
    import mock

if sys.version_info.major == 2:
    # Python 2
    import __builtin__ as builtins
else:
    # Python 3
    import builtins

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
