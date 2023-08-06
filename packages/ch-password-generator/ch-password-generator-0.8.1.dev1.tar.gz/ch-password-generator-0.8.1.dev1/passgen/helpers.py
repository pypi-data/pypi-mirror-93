"""Helper methods."""

from __future__ import unicode_literals

import random
import string

SPECIAL_CHARS = "#$%&*;:.,<>=?~"


def random_string(length, use_special=True):
    """Generates random string of given length.

    :param length: int Generated password length
    :param use_special: bool Use non-alphanumeric characters
    :returns str
    """
    allowed_chars = string.ascii_letters + string.digits
    if use_special:
        allowed_chars += SPECIAL_CHARS
    return "".join([random.choice(allowed_chars) for _ in range(length)])
