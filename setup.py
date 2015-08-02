import os
from setuptools import setup, find_packages

description = "Channel import and export tool for the BC125AT, UBC125XLT and UBC126AT."
cur_dir = os.path.dirname(__file__)
try:
	long_description = open(os.path.join(cur_dir, "README.md")).read()
except:
	long_description = description

setup(
	name = "bc125csv",
	version = "1.0.0",
	url = "http://github.com/fdev/bc125csv/",
	license = "MIT",
	description = description,
	long_description = long_description,
	author = "Folkert de Vries",
	author_email = "bc125csv@fdev.nl",
	packages = ["bc125csv"],
	install_requires = ["pyudev", "pyserial"],
	entry_points="""
	[console_scripts]
	bc125csv = bc125csv:main
	""",
	classifiers=[
		"Development Status :: 4 - Beta",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"Intended Audience :: System Administrators",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Unix",
		"Operating System :: POSIX",
		"Programming Language :: Python",
		"Topic :: Communications :: Ham Radio",
	]
)