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
		"""Parses a channel index."""
		if value is not None:
			try:
				index = int(value)
				if index in range(1, 501):
					return index
			except ValueError:
				pass
		raise ParseError("Invalid index: %s." % value)

	def parse_name(self, value):
		"""Parses and validates a channel name."""
		if value is None:
			return ""
		valid = string.ascii_letters + string.digits + "!@#$%&*()-/<>.? "
		if all(ch in valid for ch in value):
			return value
		raise ParseError("Invalid name: %s." % value)

	def parse_frequency(self, value):
		"""
		Parses and validates a channel frequency, and
		converts it to nn.mmmm string format.
		"""
		if value:
			match = self.RE_FREQ.match(value)
			if match:
				return ".".join((
					match.group(1).lstrip("0"),
					(match.group(2) or "")[:5].lstrip(".").ljust(4, "0")
				))
		raise ParseError("Invalid frequency: %s." % value)

	def parse_modulation(self, value):
		"""Parses and validates a channel modulation."""
		if value is None:
			return "AUTO"
		modulation = value.upper()
		if modulation in ("FM", "AM", "AUTO", "NFM"):
			return modulation
		raise ParseError("Invalid modulation: %s." % value)

	def parse_tqcode(self, value):
		"""Parses a channel CTCSS tone or DCS code."""
		if value is None:
			return 0

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
		
		raise ParseError("Invalid CTCSS/DCS: %s." % value)

	def parse_delay(self, value):
		"""Parses and validates a channel delay."""
		if value is None:
			return 2
		try:
			delay = int(value)
			if delay in (-10, -5, 0, 1, 2, 3, 4, 5):
				return delay
		except ValueError:
			pass

		raise ParseError("Invalid delay: %s." % value)

	def parse_flag(self, value):
		"""Parses and validates a flag."""
		if value is None:
			return False
		flag = value.lower()
		if flag in ("0", "no", "false"):
			return False
		elif flag in ("1", "yes", "true"):
			return True
		raise ParseError("Invalid flag: %s." % value)

	def parse_priority(self, value):
		"""Parses and validates a channel priority setting."""
		try:
			return self.parse_flag(value)
		except ParseError:
			raise ParseError("Invalid priority: %s." % value)

	def parse_lockout(self, value):
		"""Parses and validates a channel lockout setting."""
		try:
			return self.parse_flag(value)
		except ParseError:
			raise ParseError("Invalid lockout: %s." % value)

	def get_column(self, data, index):
		"""Safe list getter."""
		if len(data) > index and data[index]:
			return data[index]

	def parse_row(self, row):
		"""Parse a csv row to a channel object."""
		fields = (
			"index",
			"name",
			"frequency",
			"modulation",
			"tqcode",
			"delay",
			"lockout",
			"priority",
		)

		data = {}
		for index, field in enumerate(fields):
			value = self.get_column(row, index)
			fn = getattr(self, "parse_" + field)
			data[field] = fn(value)

		return Channel(**data)

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
