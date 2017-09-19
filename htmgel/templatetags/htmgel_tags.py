# Imports

# noinspection PyPackageRequirements
from django import template
# noinspection PyPackageRequirements
from django import forms
# noinspection PyPackageRequirements
from django.conf import settings
# noinspection PyPackageRequirements
from django.core.exceptions import ImproperlyConfigured
# noinspection PyPackageRequirements
from django.utils.safestring import mark_safe
from ..shortcuts import get_currency_display

register = template.Library()

# Exports

__all__ = (
    "get_attr",
    "get_index",
    "is_required_field",
    "widget_type",
)

# Constants

DEFAULT_CURRENCY = getattr(settings, "DEFAULT_CURRENCY", "USD")
ICON_FRAMEWORK = getattr(settings, "ICON_FRAMEWORK", "fontawesome")

# Tags


@register.simple_tag()
def display_currency(amount, unit=DEFAULT_CURRENCY):
    return get_currency_display(amount, unit=unit)


@register.filter("get_attr")
def get_attr(instance, name):
    """Get the value of an attribute from a given instance.

    :param instance: The instance.
    :type instance: object

    :param name: The attribute name.
    :type name: str

    """
    return getattr(instance, name)


@register.filter("get_index")
def get_index(obj, index):
    """Get the value from the given index.

    :param obj: A list or tuple.
    :type obj: list|tuple

    :param index: The index to return.
    :type index: int

    """
    try:
        return obj[index]
    except IndexError:
        return None


@register.simple_tag()
def icon(name, framework=ICON_FRAMEWORK):
    """Output an icon.

    :param name: The name of the icon.
    :type name: str

    :param framework: The icon framework to use.
    :type framework: str

    :rtype: str

    """
    # TODO: It would be a LOT of work, but we *could* validate the given icon name against the selected framework. If
    # the icon doesn't exist, we could raise an exception, log an error, or return a default.

    if framework in ("fa", "fontawesome"):
        return mark_safe('<i class="fa fa-%s" aria-hidden="true"></i>' % name)
    elif framework in ("glyph", "glyphicon"):
        return mark_safe('<span class="glyphicon glyphicon-%s" aria-hidden="true"></span>' % name)
    else:
        raise ImproperlyConfigured("Unrecognized ICON_FRAMEWORK: %s" % framework)


@register.filter("is_date")
def is_date(field):
    """Determines whether the field is a ``DateInput``."""
    return isinstance(field.field.widget, forms.DateInput)


@register.filter("is_required")
def is_required(instance):
    """Determine whether a given form field is required.

    :param instance: The instance to be checked.
    :type instance: Field

    :rtype: bool

    ..note::
        This is a shortcut to the non-intuitive means of accessing ``required``
        in a template, i.e. ``field.field.required``.

    """
    try:
        return instance.field.required
    except AttributeError:
        return instance.required


@register.filter("is_required_field")
def is_required_field(instance):
    """Determine whether a given form field is required.

    :param instance: The instance to be checked.
    :type instance: Field

    :rtype: bool

    ..note::
        This is a shortcut to the non-intuitive means of accessing ``required``
        in a template, i.e. ``field.field.required``.

    """
    try:
        return instance.field.required
    except AttributeError:
        return instance.required


@register.filter("is_select")
def is_select(field):
    return isinstance(field.field.widget, forms.Select)


@register.filter("replace")
def replace(text, from_string, to_string):
    """Replace a string."""
    return text.replace(from_string, to_string)


@register.filter("widget_type")
def widget_type(field):
    """Determine a field's widget type on the fly.

    :rtype: str

    Example:

    .. code::

        {% if field|widget_type == "Textarea" %}
            ...
        {% endif %}

    """

    try:
        return field.field.widget.__class__.__name__
    except AttributeError:
        return field.widget.__class__.__name__


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_multiple_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_radio(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)
