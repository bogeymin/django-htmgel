# Imports

from django import template

register = template.Library()

# Exports

__all__ = (
    "get_attr",
    "get_index",
    "is_required_field",
    "widget_type",
)

# Tags

@register.filter("get_attr")
def get_attr(instance, name):
    """Get the value of an attribute from a given instance.

    :param instance: The instance.
    :type instance: object

    :param: name
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
    return instance.field.required


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
    return field.field.widget.__class__.__name__
