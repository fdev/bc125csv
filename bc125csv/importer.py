from __future__ import print_function

import re
import csv
import sys
import string

from bc125csv.scanner import CTCSS_TONES, DCS_CODES, Channel


class ParseError(Exception):
	pass


class Importer(object):
	"""
	Convert CSV data read from a fileobject to channel objects.
	"""

	# Pre-compiled regular expressions
	RE_CTCSS = re.compile(r"^(?:ctcss)?\s*(\d{2,3}\.\d)\s*(?:hz)?$", re.I)
	RE_DCS = re.compile(r"^(?:dcs)?\s*(\d{2,3})$", re.I)
	RE_FREQ = re.compile(r"^(\d{1,4})(\s{0}\.\d+)?\s*(?:mhz)?$", re.I)

	def __init__(self, fh):
		self.csvreader = csv.reader(fh)

	def parse_index(self, value):
		try:
			index = int(value)
		except ValueError:
			return

		if index in range(1, 501):
			return index

	def parse_name(self, value):
		valid = string.ascii_letters + string.digits + "!@#$%&*()-/<>.? "
		if all(ch in valid for ch in value):
			return value

	def parse_frequency(self, value):
		"""Converts user-entered frequency to nn.mmmm string format."""
		match = self.RE_FREQ.match(value)
		if match:
			return ".".join((
				match.group(1).lstrip("0"),
				(match.group(2) or "")[:5].lstrip(".").ljust(4, "0")
			))

	def parse_modulation(self, value):
		value = value.upper()
		if value in ("FM", "AM", "AUTO", "NFM"):
			return value

	def parse_tq(self, value):
		"""Parse a user-defined CTCSS tone or DCS code."""
		if value in ("", "none", "all"):
			return 0
		if value in ("search",):
			return 127
		if value in ("notone", "no tone"):
			return 240

		match = self.RE_CTCSS.match(value)
		if match:
			ctcss = match.group(1).lstrip("0")
			if ctcss in CTCSS_TONES:
				return CTCSS_TONES.index(ctcss) + 64

		match = self.RE_DCS.match(value)
		if match:
			dcs = match.group(1).zfill(3)
			if dcs in DCS_CODES:
				return DCS_CODES.index(dcs) + 128

	def parse_delay(self, value):
		try:
			value = int(value)
		except ValueError:
			return

		if value in (-10, -5, 0, 1, 2, 3, 4, 5):
			return value

	def parse_flag(self, value):
		value = value.lower()
		if value in ("0", "no", "false"):
			return False
		elif value in ("1", "yes", "true"):
			return True

	def parse_row(self, data):
		"""Parse a csv row to a channel object."""
		# Channel index
		index = self.parse_index(data[0])
		if index is None:
			raise ParseError("Invalid channel %s." % data[0])

		# Name
		name = self.parse_name(data[1])
		if name is None:
			raise ParseError("Invalid name %s." % data[1])

		# Frequency
		frequency = self.parse_frequency(data[2])
		if frequency is None:
			raise ParseError("Invalid frequency %s." % data[2])

		# Modulation
		if len(data) > 3 and data[3]:
			modulation = self.parse_modulation(data[3])
			if modulation is None:
				raise ParseError("Invalid modulation %s." % data[3])
		else:
			modulation = "AUTO"

		# CTCSS/DCS
		if len(data) > 4 and data[4]:
			tq = self.parse_tq(data[4])
			if tq is None:
				raise ParseError("Invalid CTCSS/DCS %s." % data[4])
		else:
			tq = 0 # none

		# Delay
		if len(data) > 5 and data[5]:
			delay = self.parse_delay(data[5])
			if delay is None:
				raise ParseError("Invalid delay %s." % data[5])
		else:
			delay = 2

		# Lockout
		if len(data) > 6 and data[6]:
			lockout = self.parse_flag(data[6])
			if lockout is None:
				raise ParseError("Invalid lockout %s." % data[6])
		else:
			lockout = False

		# Priority
		if len(data) > 7 and data[7]:
			priority = self.parse_flag(data[7])
			if priority is None:
				raise ParseError("Invalid priority %s." % data[7])
		else:
			priority = False

		return Channel(**{
			"index":      index,
			"name":       name,
			"frequency":  frequency,
			"modulation": modulation,
			"tqcode":     tq,
			"delay":      delay,
			"lockout":    lockout,
			"priority":   priority,
		})

	def print_error(self, line, err):
		print("Error on line %d: %s" % (line, err), file=sys.stderr)

	def read(self):
		# Parsed channels
		channels = {}
		# Number of encountered errors
		errors = 0

		for row, data in enumerate(self.csvreader):
			# Skip first row (header)
			if not row:
				continue

			# Empty line
			if not data:
				continue

			# Missing required information
			if len(data) < 3:
				continue

			# Trim whitespace
			data = list(map(str.strip, data))

			# Empty channel or comment
			if not data[0] or data[0].startswith("#"):
				continue

			try:
				channel = self.parse_row(data)
			except ParseError as err:
				self.print_error(row + 1, err)
				errors += 1
				continue

			if channel.index in channels:
				self.print_error(row + 1, "Channel %d was seen before." % \
					channel.index)
				errors += 1
				continue

			channels[channel.index] = channel

		if not errors:
			return channels
