# Imports

from decimal import Decimal
from django.utils.safestring import mark_safe

# Functions


def get_currency_display(amount, unit="USD"):
    """Display a currency amount in human friendly format.

    :param amount: The amount to be displayed.
    :type amount: Decimal || int || str || unicode

    :param unit: The type of currency.
    :type unit: str || unicode

    :rtype: str

    """
    if isinstance(amount, Decimal):
        value = "{:,.2f}".format(amount)
    elif isinstance(amount, int):
        value = "{:,.2f}".format(amount)
    else:
        value = "{:,.2f}".format(int(amount))

    # Set the default symbol. Override only when the given unit is not the same.
    symbol = "$"
    if unit == "EUR":
        symbol = "&euro;"

    return mark_safe("%s%s" % (symbol, value))
