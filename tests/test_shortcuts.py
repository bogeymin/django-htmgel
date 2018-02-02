from decimal import Decimal
# import mock
import unittest
from htmgel.shortcuts import get_currency_display

# Helpers


# Tests


class TestShortcuts(unittest.TestCase):

    def test_get_current_display(self):
        """Check the format of current display."""
        output = get_currency_display("10")
        self.assertEqual("$10.00", output)

        output = get_currency_display(10)
        self.assertEqual("$10.00", output)

        output = get_currency_display(10.0)
        self.assertEqual("$10.00", output)

        output = get_currency_display(Decimal(10))
        self.assertEqual("$10.00", output)

        output = get_currency_display(10, unit="EUR")
        self.assertEqual("&euro;10.00", output)
