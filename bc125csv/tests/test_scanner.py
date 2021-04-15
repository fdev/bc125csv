from bc125csv.scanner import Channel, VirtualScanner, ScannerException
from bc125csv.tests.base import BaseTestCase


class NonRespondingScanner(VirtualScanner):
    def writeread(self, command):
        return ""


class ErrorRespondingScanner(VirtualScanner):
    def writeread(self, command):
        return "ERR"


class GarbageRespondingScanner(VirtualScanner):
    def writeread(self, command):
        return "GUVFFPNAAREVFZVFORUNIVAT"


class EnsureChannelDelete:
    def get_channel(self, index):
        return Channel(
            **{
                "index": index,
                "name": "Channel name",
                "frequency": "100.1234",
                "modulation": "FM",
                "tqcode": 0,
                "delay": 2,
                "lockout": False,
                "priority": False,
            }
        )


class ScannerTestCase(BaseTestCase):
    def test_channel(self):
        """
        Normal import into bank 1.
        """
        ch = Channel(
            **{
                "index": 1,
                "name": "Channel name",
                "frequency": "100.1234",
                "modulation": "FM",
                "tqcode": 0,
                "delay": 2,
                "lockout": False,
                "priority": False,
            }
        )
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

    def test_enter_programming(self):
        scanner = VirtualScanner()
        scanner.enter_programming()

        with self.assertRaises(ScannerException):
            scanner = NonRespondingScanner()
            scanner.enter_programming()

        with self.assertRaises(ScannerException):
            scanner = ErrorRespondingScanner()
            scanner.enter_programming()

        with self.assertRaises(ScannerException):
            scanner = GarbageRespondingScanner()
            scanner.enter_programming()

    def test_exit_programming(self):
        scanner = VirtualScanner()
        scanner.exit_programming()

        with self.assertRaises(ScannerException):
            scanner = NonRespondingScanner()
            scanner.exit_programming()

        with self.assertRaises(ScannerException):
            scanner = ErrorRespondingScanner()
            scanner.exit_programming()

        with self.assertRaises(ScannerException):
            scanner = GarbageRespondingScanner()
            scanner.exit_programming()

    def test_model(self):
        scanner = VirtualScanner()
        model = scanner.get_model()
        self.assertEqual(model, "VIRTUAL")

        with self.assertRaises(ScannerException):
            scanner = NonRespondingScanner()
            model = scanner.get_model()

        with self.assertRaises(ScannerException):
            scanner = ErrorRespondingScanner()
            model = scanner.get_model()

        with self.assertRaises(ScannerException):
            scanner = GarbageRespondingScanner()
            model = scanner.get_model()

    def test_channel_get(self):
        scanner = VirtualScanner()
        channel = scanner.get_channel(1)
        self.assertEqual(channel.name, "Channel 1")
        self.assertEqual(channel.freqcode, "01010000")
        self.assertEqual(channel.modulation, "FM")
        self.assertEqual(channel.delay, 2)

        with self.assertRaises(ScannerException):
            scanner = NonRespondingScanner()
            channel = scanner.get_channel(1)

        with self.assertRaises(ScannerException):
            scanner = ErrorRespondingScanner()
            channel = scanner.get_channel(1)

        with self.assertRaises(ScannerException):
            scanner = GarbageRespondingScanner()
            channel = scanner.get_channel(1)

    def test_channel_set(self):
        ch = Channel(
            **{
                "index": 1,
                "name": "Channel name",
                "frequency": "100.1234",
                "modulation": "FM",
                "tqcode": 0,
                "delay": 2,
                "lockout": False,
                "priority": False,
            }
        )

        scanner = VirtualScanner()
        scanner.set_channel(ch)

        with self.assertRaises(ScannerException):
            scanner = NonRespondingScanner()
            scanner.set_channel(ch)

        with self.assertRaises(ScannerException):
            scanner = ErrorRespondingScanner()
            scanner.set_channel(ch)

        with self.assertRaises(ScannerException):
            scanner = GarbageRespondingScanner()
            scanner.set_channel(ch)

    def test_channel_delete(self):
        scanner = VirtualScanner()
        scanner.delete_channel(1)

        class NonRespondingDelete(EnsureChannelDelete, NonRespondingScanner):
            pass

        with self.assertRaises(ScannerException):
            scanner = NonRespondingDelete()
            scanner.delete_channel(1)

        class ErrorRespondingDelete(EnsureChannelDelete, NonRespondingScanner):
            pass

        with self.assertRaises(ScannerException):
            scanner = ErrorRespondingDelete()
            scanner.delete_channel(1)

        class GarbageRespondingDelete(
            EnsureChannelDelete, NonRespondingScanner
        ):
            pass

        with self.assertRaises(ScannerException):
            scanner = GarbageRespondingDelete()
            scanner.delete_channel(1)
