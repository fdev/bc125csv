bc125csv
=============

Channel import and export tool for the Uniden BC125AT, UBC125XLT, UBC126AT, and SR30C.

[![Build Status](https://travis-ci.org/fdev/bc125csv.svg)](https://travis-ci.org/fdev/bc125csv)
[![Code Climate](https://codeclimate.com/github/fdev/bc125csv/badges/gpa.svg)](https://codeclimate.com/github/fdev/bc125csv)
[![Code Health](https://landscape.io/github/fdev/bc125csv/master/landscape.svg?style=flat)](https://landscape.io/github/fdev/bc125csv/master)


Introduction
------------
bc125csv provides a simple command-line interface for importing and 
exporting the channels on your Uniden Bearcat scanner in CSV file format.

This application is not intended to provide full control of *all* features on
your scanner; if you want to turn off the backlight in your scanner, just turn
the knob and press some buttons. This application *does* however aim to lessen
the amount of work needed for entering channels considerably, especially for 
those on Linux or UNIX-like systems.


If you do feel the need to change the backlight setting on your scanner using
the command-line, the shell action will allow you to do so (see [Examples](#examples)).


Requirements
------------

* Python 2.7+ or 3.4+
* [pySerial](http://pyserial.sourceforge.net/)

Both pyudev and pySerial will be automatically installed on installation.

You can use this application without a connected scanner by enabling the virtual
scanner device using the `--no-scanner` option.


Installation
------------

On most UNIX-like systems, you can install bc125csv by running one of the 
following install commands with root privileges.

```
git clone git://github.com/fdev/bc125csv.git
cd bc125csv
python setup.py install
```

*or*

```
pip install git+http://github.com/fdev/bc125csv
```


Tests
-----

This application aims to cover 100% of its code with tests, though some 
parts that require a physical device to be attached are skipped. 

To run the tests, you can run the following command:

```
nosetests --with-coverage --cover-package=bc125csv
```

Continuous integration is done by Travis.


Usage
-----

```
Usage: bc125csv ACTION [OPTIONS]
-b, --banks BANKS    Only process given banks.
                     Separate multiple banks with spaces.
-e, --include-empty  Include empty channels in export.
-h, --help           Display this help and exit.
                     Use command help for detailed instructions.
-i, --input FILE     Read from file when importing.
-n, --no-scanner     Use a virtual scanner device.
-o, --output FILE    Write to file when exporting.
-r, --rate           Baud rate (default 9600).
-s, --sparse         Omit 'no' and 'none' values in export.
-v, --verbose        Be more verbose.
-V, --version        Output version information and exit.

Available actions are:
  verify  - Verify csv data (no device needed).
  import  - Import channels to the scanner in csv format.
  export  - Export channels from the scanner in csv format.
  shell   - Start an interactive shell with the device.
  help    - Display detailed help.
```


Examples
--------

**Exporting banks 1, 2 and 3**
```
bc125csv export -s -b 1 2 3 > banks-123.csv
```

**Importing from csv file**
```
bc125csv import < channels.csv
```

**Verify a csv file**
```
bc125csv verify -v -i channels.csv
```

**Enable backlight using the shell**
```
echo -en "PRG\nBLT,AO\nEPG" | bc125csv shell
```


Export format
-------------

The export format is a comma separated values file with header,
comments and empty lines to improve readability. Empty channels
are omitted by default, but can be included using the `--include-empty` 
option. Any 'no' and 'none' values in the CTCSS/DCS, Lockout and 
Priority columns can be omitted by using the `--sparse` option.


```
Channel,Name,Frequency,Modulation,CTCSS/DCS,Delay,Lockout,Priority

# Bank 1
1,PMR Channel 1,446.0062,FM,none,2,no,no
2,PMR Channel 2,446.0187,FM,no tone,2,no,no
3,Private channel,446.0187,FM,DCS 155,3,no,yes

# Bank 2
51,PMR Channel 3,446.0312,FM,no tone,3,no,no
52,Construction,446.0312,FM,114.8 Hz,1,no,yes
56,Hot Air Balloons,122.2500,AM,none,2,no,no
```


Import format
-------------

The import format is the same as the export format, but forgiving:

 * CTCSS/DCS, Delay, Lockout and Priority values may be left empty,
 * no, false, 0 and <empty> may be used interchangeably,
 * yes, true and 1 may be used interchangeably,
 * CTCSS tones may be written as 114.8, 114.8Hz, CTCSS 114.8 Hz, etc,
 * DCS codes may be written as 26, 026, DCS026, DCS 026,
 * lines beginning with a `#` (comment line) or `,` (no channel) and 
   the first line (containing the header) are ignored,
 * additional columns are ignored,
 * frequencies are automatically rounded down to 4 decimal places.


Shell
-----
You can start an interactive shell to send commands to your scanner.
See the [BC125AT Operation Specification][proto] for all available commands.

```
$ bc125csv shell
> MDL
< MDL,UBC125XLT
> VER
< VER,Version 1.00.06
```

You can also pipe commands into your scanner. The following example enters
programming mode, enables the backlight, and then exits programming mode.

```
echo -en "PRG\nBLT,AO\nEPG" | bc125csv shell
```

The wary reader might have noticed the Operation Specification dictates commands
be terminated by a carriage return. This application automatically appends the
carriage return to each command it sends to the scanner. There's no need to
include a carriage return yourself.


Compatibility
-------------

This application is compatible with the Uniden Bearcat models BC125AT, UBC125XLT,
UBC126AT, and SR30C.

Note: the SR30C uses a stock UART serial USB chipset (specifically, the CP2104).
Linux kernel v2.6.12+ appears to have the driver, but in other operating systems
it may be necessary to get drivers from the manufacturer:
https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers


License (MIT)
-------------

Copyright (c) 2020, Folkert de Vries <bc125csv@fdev.nl>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Disclaimer
----------

Uniden® and Bearcat® are registered trademarks of Uniden America Corporation. 
This application and its author are not affiliated with or endorsed by Uniden
in any way.


[proto]: http://info.uniden.com/twiki/pub/UnidenMan4/BC125AT/BC125AT_Protocol.pdf
