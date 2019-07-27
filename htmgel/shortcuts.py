# Imports

from decimal import Decimal
from django.utils.safestring import mark_safe
from django.template import Context, loader, Template, TemplateDoesNotExist

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

def parse_template(template, context):
    """Ad hoc means of parsing a template using Django's built-in loader.

    :param template: The name of the template.
    :type template: str || unicode

    :param context: Context variables.
    :type context: dict

    :rtype: str

    """
    return loader.render_to_string(template, context)
