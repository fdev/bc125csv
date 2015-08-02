from bc125csv import main
from bc125csv.scanner import Channel
from bc125csv.tests.base import BaseTestCase, mock


class ScannerTestCase(BaseTestCase):
	def test_channel(self):
		"""
		Normal import into bank 1.
		"""
		ch = Channel(**{
			"index": 1,
			"name": "Channel name",
			"frequency": "100.1234",
			"modulation": "FM",
			"tqcode": 0,
			"delay": 2,
			"lockout": False,
			"priority": False,
		})
		self.assertEqual(str(ch), "CH001: 100.1234 FM")
		self.assertEqual(ch.freqcode, "01001234")
		self.assertEqual(ch.tq, "none")

		ch.tqcode = 127
		self.assertEqual(ch.tq, "search")

		ch.tqcode = 240
		self.assertEqual(ch.tq, "no tone")

		ch.tqcode = 84
		self.assertEqual(ch.tq, "131.8 Hz")

		ch.tqcode = 148
		self.assertEqual(ch.tq, "DCS 125")
