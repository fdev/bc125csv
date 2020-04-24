"""
bc125csv - Channel import and export tool for the Uniden BC125AT, UBC125XLT 
and UBC126AT.

Copyright (c) 2020, fdev.nl. All rights reserved.
Released under the MIT license.

Uniden and Bearcat are registered trademarks of Uniden America Corporation.
This application and its author are not affiliated with or endorsed by Uniden
in any way.
"""

__author__ = "Folkert de Vries"
__email__ = "bc125csv@fdev.nl"
__version__ = "1.0.2"
__date__ = "Apr 24, 2020"

# Expose main function for setup.py console_scripts
from bc125csv.handler import main
