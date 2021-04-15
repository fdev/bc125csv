import re
import sys

try:
    import serial
    from serial.tools.list_ports import comports
except ImportError:
    sys.exit(
        "Failed to import pyserial (http://pyserial.sourceforge.net/),"
        " install using:\n  pip install pyserial"
    )


# Keep single line formatting of lists.
# fmt: off

# CTCSS (Continuous Tone-Coded Squelch System) tones
CTCSS_TONES = [
    "67.0", "69.3", "71.9", "74.4", "77.0", "79.7", "82.5", "85.4",
    "88.5", "91.5", "94.8", "97.4", "100.0", "103.5", "107.2", "110.9",
    "114.8", "118.8", "123.0", "127.3", "131.8", "136.5", "141.3", "146.2",
    "151.4", "156.7", "159.8", "162.2", "165.5", "167.9", "171.3", "173.8",
    "177.3", "179.9", "183.5", "186.2", "189.9", "192.8", "196.6", "199.5",
    "203.5", "206.5", "210.7", "218.1", "225.7", "229.1", "233.6", "241.8",
    "250.3", "254.1",
]

# DCS (Digital-Coded Squelch) codes
DCS_CODES = [
    "023", "025", "026", "031", "032", "036", "043", "047", "051", "053",
    "054", "065", "071", "072", "073", "074", "114", "115", "116", "122",
    "125", "131", "132", "134", "143", "145", "152", "155", "156", "162",
    "165", "172", "174", "205", "212", "223", "225", "226", "243", "244",
    "245", "246", "251", "252", "255", "261", "263", "265", "266", "271",
    "274", "306", "311", "315", "325", "331", "332", "343", "346", "351",
    "356", "364", "365", "371", "411", "412", "413", "423", "431", "432",
    "445", "446", "452", "454", "455", "462", "464", "465", "466", "503",
    "506", "516", "523", "526", "532", "546", "565", "606", "612", "624",
    "627", "631", "632", "654", "662", "664", "703", "712", "723", "731",
    "732", "734", "743", "754",
]

# Restore formatting.
# fmt: on


class Channel:
    """
    Representation of a channel in the scanner.
    """

    def __init__(
        self,
        index,
        name,
        frequency,
        modulation="AUTO",
        tqcode=0,
        delay=2,
        lockout=False,
        priority=False,
    ):
        self.index = index
        self.name = name
        self.frequency = frequency
        self.modulation = modulation
        self.tqcode = tqcode
        self.delay = delay
        self.lockout = lockout
        self.priority = priority

    @property
    def tq(self):
        """Readable CTCSS tone and DCS code."""
        if self.tqcode == 0:
            return "none"
        if self.tqcode == 127:
            return "search"
        if self.tqcode == 240:
            return "no tone"
        if 64 <= self.tqcode <= 113:
            return CTCSS_TONES[self.tqcode - 64] + " Hz"
        if 128 <= self.tqcode <= 231:
            return "DCS " + DCS_CODES[self.tqcode - 128]
        return ""

    @property
    def freqcode(self):
        """Frequency code in CIN format (nnnnmmmm)."""
        return self.frequency.replace(".", "").zfill(8)

    def __repr__(self):
        return "CH%03d: %s %s" % (self.index, self.frequency, self.modulation)


class ScannerException(Exception):
    pass


class Scanner(serial.Serial):
    """
    Wrap around Serial to provide compatible readline and helper methods.
    """

    RE_CIN = re.compile(
        r"""
        # CIN,[INDEX],[NAME],[FRQ],[MOD],[CTCSS/DCS],[DLY],[LOUT],[PRI]
        ^ # No characters before
        CIN,
        (?P<index>\d{1,3}),
        (?P<name>[^,]{0,16}),
        (?P<freq>\d{5,8}), # 4 decimals, so at least 5 digits
        (?P<modulation>|AUTO|AM|FM|NFM), # can be empty for SR30C
        (?P<tq>\d{0,3}), # can be empty for SR30C
        (?P<delay>-10|-5|0|1|2|3|4|5),
        (?P<lockout>0|1),
        (?P<priority>0|1) # no comma!
        $ # No characters after
        """,
        flags=re.VERBOSE,
    )

    def __init__(self, port, baudrate=9600):
        super(Scanner, self).__init__(port=port, baudrate=baudrate)

    def writeread(self, command):
        self.write((command + "\r").encode())
        self.flush()
        return self.readlinecr()

    def send(self, command):
        result = self.writeread(command)
        if not re.match(r"(^ERR|,NG$)", result):
            return result
        return None

    def readlinecr(self):
        """
        The Serial class might be based on serial.FileLike, which allows
        one to override the eol character, and io.RawIOBase, which doesn't.
        To ensure this possibility, the readline method is overriden.
        """
        line = ""
        while True:
            c = self.read(1).decode()
            if c == "\r":
                return line
            line += c

    def enter_programming(self):
        result = self.send("PRG")
        if not result or result != "PRG,OK":
            raise ScannerException("Failed to enter programming mode.")

    def exit_programming(self):
        result = self.send("EPG")
        if not result or result != "EPG,OK":
            raise ScannerException("Failed to leave programming mode.")

    def get_model(self):
        """Get model name from scanner."""
        result = self.send("MDL")
        if not result or not result.startswith("MDL,"):
            raise ScannerException("Could not get model name.")
        return result[4:]

    def get_channel(self, index):
        """Read channel object from scanner."""
        result = self.send("CIN,%d" % index)

        # Error occurred
        if not result:
            raise ScannerException("Could not read channel %d." % index)

        # Try to match result
        match = self.RE_CIN.match(result)
        if not match:
            raise ScannerException("Unexpected data for channel %d." % index)
        data = match.groupdict()

        # Return on empty channel
        if data["freq"] == "00000000":
            return None

        # Convert 1290000 to 129.0000
        frequency = "%s.%s" % (
            data["freq"][:-4].lstrip("0"),
            data["freq"][-4:],
        )

        return Channel(
            **{
                "index": int(data["index"]),
                "name": data["name"].strip(),
                "frequency": frequency,
                # Default to "AUTO" for empty values returned by SR30C.
                "modulation": data["modulation"] or "AUTO",
                # Default to "0" for empty values returned by SR30C.
                "tqcode": int(data["tq"] or "0"),
                "delay": int(data["delay"]),
                "lockout": data["lockout"] == "1",
                "priority": data["priority"] == "1",
            }
        )

    def set_channel(self, channel):
        """Write channel object to scanner."""
        command = ",".join(
            map(
                str,
                [
                    "CIN",
                    channel.index,
                    channel.name,
                    channel.freqcode,
                    channel.modulation,
                    channel.tqcode,
                    channel.delay,
                    int(channel.lockout),
                    int(channel.priority),
                ],
            )
        )

        # Write to scanner
        result = self.send(command)
        if not result or result != "CIN,OK":
            raise ScannerException(
                "Could not write to channel %d." % channel.index
            )

    def delete_channel(self, index):
        """Delete channel from scanner."""
        channel = self.get_channel(index)

        # Only delete if channel has data
        # Unnecessary deletes are slow
        if channel:
            result = self.send("DCH,%d" % index)
            if not result or result != "DCH,OK":
                raise ScannerException("Could not delete channel %d." % index)


class VirtualScanner(Scanner):
    """
    Virtual scanner to test without an actual scanner.
    """

    def __init__(self, *args, **kwargs):
        # Don"t create a Serial object
        pass

    def writeread(self, command):
        """Fake the handling of certain commands."""
        # Get model
        if command == "MDL":
            return "MDL,VIRTUAL"

        # Programming mode
        if command == "PRG":
            return "PRG,OK"

        # Exit programming mode
        if command == "EPG":
            return "EPG,OK"

        # Get channel
        if re.match(r"^CIN,([1-9]|1[0-9]|5[1-9])$", command):
            # Return data for channels 1-19 and 51-59
            index = int(command[4:])
            lockout = index == 55
            priority = index == 15
            return "CIN,{0},Channel {0},1{0:02d}0000,FM,0,2,{1:d},{2:d}".format(
                index, lockout, priority
            )

        elif re.match(r"^CIN,[0-9]+$", command):
            index = int(command[4:])
            tq = (0, 127, 240, 145)[index % 4]
            return "CIN,{0},,00000000,FM,{1},0,0,0".format(index, tq)

        # Set channel
        if command.startswith("CIN,"):
            return "CIN,OK"

        # Delete channel
        if command.startswith("DCH,"):
            return "DCH,OK"

        # Other commands give an error
        return "ERR"


class Device:
    """
    Detected serial USB device.
    """

    def __init__(self, path, baudrate):
        self.path = path
        self.baudrate = baudrate

    @staticmethod
    def lookup():
        """Find compatible scanner and return Device instance."""
        ports = comports(include_links=False)

        for port in ports:
            # Uniden vendor
            if port.vid == 6501 and port.product in (
                "BC125AT",
                "UBC125XLT",
                "UBC126AT",
            ):
                return Device(path=port.device, baudrate=9600)

            # Silicon Laboratories vendor (SR30C uses this chipset)
            if port.vid == 4292 and port.pid == 60000:
                return Device(path=port.device, baudrate=57600)

        return None
