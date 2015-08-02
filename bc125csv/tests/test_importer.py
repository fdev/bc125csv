from bc125csv import main
from bc125csv.tests.base import BaseTestCase, PseudoTTY, StringIO, mock, builtins


class ImporterTestCase(BaseTestCase):
	def test_import(self):
		"""
		Normal import into bank 1.
		"""
		with mock.patch("os.path.isfile", return_value=True):
			with mock.patch.object(builtins, 'open', return_value=StringIO(IMPORT)):
				main(["import", "-n", "-b", "1", "-i", "import.csv"])

	def test_import_errors(self):
		"""
		Invalid import into bank 2.
		"""
		with mock.patch("os.path.isfile", return_value=True):
			with mock.patch.object(builtins, 'open', return_value=StringIO(IMPORT_ERRORS)):
				with self.assertRaises(SystemExit) as cm:
					main(["import", "-n", "-b", "2", "-i", "import_errors.csv"])
				self.assertNotEqual(cm.exception.code, None)

	def test_import_nofile(self):
		"""
		Non-existing file import.
		"""
		with mock.patch("os.path.isfile", return_value=False):
			with self.assertRaises(SystemExit) as cm:
				main(["import", "-n", "-i", "doesnotexist.csv"])
			self.assertNotEqual(cm.exception.code, None)

	def test_import_stdin(self):
		"""
		Import from stdin.
		"""
		with mock.patch("sys.stdin", StringIO(IMPORT)):
			main(["import", "-n"])

IMPORT = """Channel,Name,Frequency,Modulation,CTCSS/DCS,Delay,Lockout,Priority
#Channel,Name,Frequency,Modulation,CTCSS/DCS,Delay,Lockout,Priority

# Bank 1
1,Channel Name,100.0000

# Modulations
2,Channel Name,100.0000,AUTO
3,Channel Name,100.0000,FM
4,Channel Name,100.0000,NFM
5,Channel Name,100.0000,AM

# TQ
6,Channel Name,100.0000,,none
7,Channel Name,100.0000,,DCS 261,2
8,Channel Name,100.0000,,search
9,Channel Name,100.0000,,no tone
10,Channel Name,100.0000,,CTCSS 136.5 Hz

# Delay
11,Channel Name,100.0000,,,2

# Lockout
12,Channel Name,100.0000,,,,yes
13,Channel Name,100.0000,,,,no

# Priority
14,Channel Name,100.0000,,,,,yes
15,Channel Name,100.0000,,,,,no
"""

IMPORT_ERRORS = """Channel,Name,Frequency,Modulation,CTCSS/DCS,Delay,Lockout,Priority

# Name
1,Channel name too long,100.0000
2,Wrong chars~~~,100.0000

# Frequency
3,Channel name,100.999x
3,Channel name,-100.000
# Modulation
4,Channel name,100.0000,XM
# TQ
5,Channel name,100.0000,,error
# Delay
6,Channel name,100.0000,,,99
7,Channel name,100.0000,,,error

# Lockout
8,Channel name,100.0000,,,,error
# Priority
9,Channel name,100.0000,,,,,error

# Channel
error,Channel name,100.0000
1000,Channel name,100.0000
1,Duplicate index,100.0000
"""
