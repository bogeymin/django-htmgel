# Imports

from .html import BaseHTML

# Exports

# Classes


class Fieldset(BaseHTML):
    """A fieldset within a form."""

    def __init__(self, legend, fields=None, **kwargs):
        super(Fieldset, self).__init__(legend, open_tag="fieldset")
        self.fields = fields or list()

    def __iter__(self):
        return iter(self.fields)

    def add_field(self, field):
        """Add a field to the fieldset.

        :param field: The field instance from the form.

        """
        self.fields.append(field)

    def to_html(self):
        a = list()
        a.append("<%s>" % self.get_open_tag())

        a.append("<legend>%s</legend>" % self.content)

        for f in self.fields:
            a.append(str(f))

        a.append("<%s>" % self.get_close_tag())

        return "\n".join(a)
