from __future__ import print_function

import csv


class Exporter(object):
	"""
	Convert channel objects to CSV data and write to file object.
	"""

	def write(self, channels, fh, sparse=False):
		csvwriter = csv.writer(fh, lineterminator="\n")
		
		# Helper function
		def write(row=None):
			csvwriter.writerow(row or [])

		# Header
		write([
			"Channel",
			"Name",
			"Frequency",
			"Modulation",
			"CTCSS/DCS",
			"Delay",
			"Lockout",
			"Priority",
		])
		
		# Iterate over all banks
		for bank in range(1, 11):
			bankheader = False
			
			for index in range(bank * 50 - 49, bank * 50 + 1):
				if index not in channels:
					continue

				if not bankheader:
					write()
					write(["# Bank %d" % bank])
					bankheader = True

				channel = channels[index]

				if not channel:
					write([index])
					continue

				if channel.lockout:
					lockout = "yes"
				elif sparse:
					lockout = ""
				else:
					lockout = "no"

				if channel.priority:
					priority = "yes"
				elif sparse:
					priority = ""
				else:
					priority = "no"

				write([
					# Channel
					channel.index,
					# Name
					channel.name,
					# Frequency
					channel.frequency,
					# Modulation
					channel.modulation,
					# CTCSS/DCS
					"" if channel.tqcode == 0 and sparse else channel.tq,
					# Delay
					channel.delay,
					# Lockout
					lockout,
					# Priority
					priority,
				])

