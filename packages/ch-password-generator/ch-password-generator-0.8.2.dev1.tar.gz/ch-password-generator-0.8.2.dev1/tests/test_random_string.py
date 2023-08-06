"""Tests for password generation method."""

from __future__ import unicode_literals
from passgen.helpers import random_string, SPECIAL_CHARS


def test_random_string_length():
    """Test that generated password has desired length."""
    random_length = 20
    password = random_string(length=random_length)
    assert len(password) == random_length


def test_random_string_without_special_characters():
    """
    This test may actually fail as it checks random functionality. It's possible that one of 10000 randomly
    generated passwords will not contain SPECIAL_CHARS by pure accident and not because such option were used.
    But we can assume it should work in most cases.
    """
    for _ in range(10000):
        password = random_string(length=64, use_special=False)
        assert not any([x for x in SPECIAL_CHARS if x in password])
