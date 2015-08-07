from bc125csv import main
from bc125csv.handler import VERSION
from bc125csv.tests.test_importer import IMPORT, IMPORT_ERRORS
from bc125csv.tests.base import BaseTestCase, PseudoTTY, StringIO, mock, builtins

from bc125csv.tests.base import unittest

class HandlerTestCase(BaseTestCase):
	def test_version(self):
		"""
		Show version.
		"""
		with self.assertRaises(SystemExit) as cm:
			main(["-V"])
		self.assertStdOut(VERSION)
		self.assertEqual(cm.exception.code, None)

	def test_usage(self):
		"""
		Show usage.
		"""
		with self.assertRaises(SystemExit) as cm:
			main([])
		self.assertEqual(cm.exception.code, None)

	def test_help(self):
		"""
		Show help.
		"""
		with self.assertRaises(SystemExit) as cm:
			main(["help"])
		self.assertEqual(cm.exception.code, None)

	def test_verify_stdin(self):
		"""
		Verify csv data from stdin.
		"""
		with mock.patch("sys.stdin", StringIO(IMPORT)):
			with self.assertRaises(SystemExit) as cm:
				main(["verify"])
			self.assertStdOut("")
			self.assertStdErr("")
			self.assertEqual(cm.exception.code, None)

	def test_verify_errors(self):
		"""
		Verify csv data from file with errors.
		"""
		with mock.patch("os.path.isfile", return_value=True):
			with mock.patch.object(builtins, 'open', return_value=StringIO(IMPORT_ERRORS)):
				with self.assertRaises(SystemExit) as cm:
					main(["verify", "-v", "-i", "import_errors.csv"])
				self.assertStdOut("")
				self.assertStdErr(ERROR_LINES)
				self.assertNotEqual(cm.exception.code, None)

	def test_verify_file(self):
		"""
		Verify csv data from file.
		"""
		with mock.patch("os.path.isfile", return_value=True):
			with mock.patch.object(builtins, 'open', return_value=StringIO(IMPORT)):
				with self.assertRaises(SystemExit) as cm:
					main(["verify", "-v", "-i", "import.csv"])
				self.assertStdOut("")
				self.assertStdErr("No errors found.")
				self.assertEqual(cm.exception.code, None)

	def test_verify_nofile(self):
		"""
		Verify csv data from non-existing file.
		"""
		with mock.patch("os.path.isfile", return_value=False):
			with self.assertRaises(SystemExit) as cm:
				main(["verify", "-v", "-i", "doesnotexist.csv"])
			self.assertStdErr("")
			self.assertNotEqual(cm.exception.code, None)

	#@unittest.skipIf(sys.version_info[0] < 3, 'Python 3')
	def test_shell(self):
		"""
		Test interactive shell
		"""
		with mock.patch("sys.stdin", StringIO("PRG\n\nBLT,AO\nEPG")):
			with self.assertRaises(SystemExit) as cm:
				main(["shell", "-n"])
			self.assertEqual(cm.exception.code, None)

		with mock.patch("sys.stdin", PseudoTTY(StringIO("PRG\n\nBLT,AO\nEPG"))):
			with self.assertRaises(SystemExit) as cm:
				main(["shell", "-n"])
			self.assertEqual(cm.exception.code, None)

ERROR_LINES = """Error on line 5: Invalid name: Wrong chars~~~.
Error on line 8: Invalid frequency: 100.999x.
Error on line 9: Invalid frequency: -100.000.
Error on line 11: Invalid modulation: XM.
Error on line 13: Invalid CTCSS/DCS: error.
Error on line 15: Invalid delay: 99.
Error on line 16: Invalid delay: error.
Error on line 19: Invalid lockout: error.
Error on line 21: Invalid priority: error.
Error on line 24: Invalid index: error.
Error on line 25: Invalid index: 1000.
Error on line 26: Channel 1 was seen before."""
