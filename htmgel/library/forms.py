# Imports

from django.utils.safestring import mark_safe
from .html import BaseHTML

# Exports

__all__ = (
    "Fieldset",
)

# Classes


class Fieldset(BaseHTML):
    """A fieldset within a form."""

    def __init__(self, legend, fields=None, **kwargs):
        kwargs['open_tag'] = "fieldset"
        super(Fieldset, self).__init__("", **kwargs)

        self.fields = fields or list()
        self.legend = legend

    def __iter__(self):
        return iter(self.fields)

    def add_field(self, field):
        """Add a field to the fieldset.

        :param field: The field instance from the form.

        """
        self.fields.append(field)

    @mark_safe
    def to_html(self):
        a = list()
        a.append("<%s>" % self.get_open_tag())

        a.append("<legend>%s</legend>" % self.legend)

        for f in self.fields:
            a.append(str(f))

        a.append("<%s>" % self.get_close_tag())

        return "\n".join(a)
