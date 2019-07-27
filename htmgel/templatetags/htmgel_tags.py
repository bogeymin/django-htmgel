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
import os
from ..shortcuts import get_currency_display, parse_template

register = template.Library()

# Exports

__all__ = (
    "display_currency",
    "get_attr",
    "get_index",
    "icon",
    "is_checkbox",
    "is_clearable_file",
    "is_date",
    "is_datetime",
    "is_file",
    "is_hidden",
    "is_markdown",
    "is_multiple_checkbox",
    "is_password",
    "is_radio",
    "is_required",
    "is_select",
    "is_select_multiple",
    "is_text",
    "replace",
)

# Constants

DEFAULT_CURRENCY = getattr(settings, "DEFAULT_CURRENCY", "USD")
ICON_FRAMEWORK = getattr(settings, "ICON_FRAMEWORK", "fontawesome")

if "htmgel_bootstrap3" in settings.INSTALLED_APPS:
    HTML_FRAMEWORK = "bootstrap3"
elif "htmgel_bootstrap4" in settings.INSTALLED_APPS:
    HTML_FRAMEWORK = "bootstrap4"
else:
    raise ImproperlyConfigured("HTML framework is not installed.")

# General Tags


@register.simple_tag()
def display_currency(amount, unit=DEFAULT_CURRENCY):
    return get_currency_display(amount, unit=unit)


@register.filter
def get_attr(instance, name):
    """Get the value of an attribute from a given instance.

    :param instance: The instance.
    :type instance: object

    :param name: The attribute name.
    :type name: str

    """
    return getattr(instance, name)


@register.filter
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


@register.simple_tag(takes_context=True)
def html(context, path, **kwargs):
    if ".html" not in path:
        path += ".html"

    template_path = os.path.join("htmgel", path)

    # print("PATH =", template_path)
    # print("CONTEXT =", context)
    # print("-" * 80)

    # The context argument is a RequestContext which is *not* a dictionary, but a contains a list of dictionaries that
    # is iterable. To pass the context, we need to process each dictionary.
    _context = dict()
    for d in context:
        _context.update(d)

    # Add keyword arguments passed to the tag. These are specific to the template being loaded.
    _context.update(kwargs)

    return parse_template(template_path, _context)


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


@register.filter
def replace(text, from_string, to_string):
    """Replace a string."""
    return text.replace(from_string, to_string)

# Field-Related Tags


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_clearable_file(field):
    return isinstance(field.field.widget, forms.ClearableFileInput)


@register.filter
def is_date(field):
    """Determines whether the field is a ``DateInput``."""
    return isinstance(field.field.widget, forms.DateInput)


@register.filter
def is_datetime(field):
    return isinstance(field.field.widget, forms.DateTimeInput)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def is_hidden(field):
    return isinstance(field.field.widget, forms.HiddenInput)


@register.filter
def is_markdown(field):
    return field.field.widget.__class__.__name__ == "MarkdownWidget"


@register.filter
def is_multiple_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_password(field):
    return isinstance(field.field.widget, forms.PasswordInput)


@register.filter
def is_radio(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_required(field):
    """Determine whether a given form field is required.

    :param field: The instance to be checked.
    :type field: Field

    :rtype: bool

    ..note::
        This is a shortcut to the non-intuitive means of accessing ``required``
        in a template, i.e. ``field.field.required``.

    """
    try:
        return field.field.required
    except AttributeError:
        return field.required


@register.filter
def is_select(field):
    return isinstance(field.field.widget, forms.Select)


@register.filter
def is_select_multiple(field):
    return isinstance(field.field.widget, forms.SelectMultiple)


@register.filter
def is_text(field):
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
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
