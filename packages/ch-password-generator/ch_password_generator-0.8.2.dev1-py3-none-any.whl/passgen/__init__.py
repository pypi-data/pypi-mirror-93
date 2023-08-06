"""CLI interface."""

from __future__ import unicode_literals
from __future__ import print_function

import argparse
from passgen.helpers import random_string

DESCRIPTION = "Simple random password generator."
DEFAULT_LEN = 20  # Default length if no arguments provided


def main():  # pragma: no cover
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "-l",
        "--length",
        dest="length",
        default=DEFAULT_LEN,
        type=int,
        help="Specify length for generated password",
    )
    parser.add_argument(
        "-s",
        "--simple",
        action="store_false",
        dest="simple",
        help="Use only alphanumeric characters (without #@... etc.)",
    )
    arguments = parser.parse_args()
    print(random_string(arguments.length, use_special=arguments.simple))
