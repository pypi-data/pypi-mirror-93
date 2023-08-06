"""Tests for actual program command."""

import passgen
from passgen import __main__  # noqa


class FakeApp(object):
    """Fake method factory."""

    @staticmethod
    def main():
        """Fake '__main__' run."""
        passgen.main()


# pylint: disable=no-member
def test_passgen_program_call(mocker):
    """Mock program run."""
    mocker.patch("passgen.main")
    FakeApp.main()
    passgen.main.assert_called_once()  # noqa
