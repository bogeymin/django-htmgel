# Imports

from copy import deepcopy
from django.forms.utils import flatatt
from django.urls import reverse
from django.utils.safestring import mark_safe

# Exports

__all__ = (
    "BaseHTML",
    "Anchor",
    "Table",
    "TableColumn",
    "TableRow",
)

# Classes


class BaseHTML(object):
    """Base class for creating HTML objects."""

    def __init__(self, **kwargs):
        """Initialize an HTML element.

        .. tip::
            We can't use the ``class`` as a keyword, so we provide for CSS classes with a special ``classes`` attribute
            which may be given as a ``str`` or ``list``.

        """
        self._classes = kwargs.pop("classes", "")
        self._attributes = kwargs

    def get_attributes(self):
        """Get attributes for the element.

        :rtype: dict

        .. warning::
            If you override this method, you *must* account for the ``classes`` attribute.

        """
        attrs = self._attributes.copy()

        if isinstance(self._classes, list):
            attrs['class'] = " ".join(self._classes)
        elif isinstance(self._classes, basestring):
            attrs['class'] = self._classes
        else:
            pass

        return attrs

    def to_html(self):
        """Get the element as HTML.

        :rtype: str

        """
        raise NotImplementedError()


class Anchor(BaseHTML):
    """Represents a link (URL)."""

    def __init__(self, href, text=None, **kwargs):
        """Initialize an HTML anchor.

        :param href: The URL of the link.
        :type href: str

        :param text: The link text to display. Defaults to the ``href``.
        :type text: str

        ``kwargs`` may be any valid anchor attribute.

        """
        self.href = href
        self.name = kwargs.pop("name")
        self.target = kwargs.pop("target")
        self.title = kwargs.pop("title")
        self.text = text or href

        super(Anchor, self).__init__(**kwargs)

    def get_attributes(self):
        """If ``name`` is given, only the name is returned in the dict."""
        if self.name:
            return {'name': self.name}

        a = {'href': self.href}

        if self.target:
            a['target'] = self.target

        if self.title:
            a['title'] = self.title

        return a

    def to_html(self):
        """If ``name`` is given, a named anchor is returned."""
        if self.name:
            return mark_safe('<a name="%s">' % self.name)

        attrs = self.get_attributes()
        html = '<a %s>%s</a>' % (flatatt(attrs), self.text)

        return mark_safe(html)


class Breadcrumb(object):
    """Helper class that ensures an object has the required attributes."""

    def __init__(self, title=None, url=None):
        self.title = title
        self.url = url

    def get_absolute_url(self):
        return self.url


class Breadcrumbs(object):
    """Collect objects to be displayed as breadcrumbs."""

    def __init__(self):
        self.items = list()

    def __iter__(self):
        return iter(self.items)

    def add(self, item):
        """Add to the breadcrumb list.
        
        :param item: The item to be added.  
        :type item: Breadcrumb

        """
        self.items.append(item)

    def append(self, label, url, pattern_args=None, pattern_kwargs=None):
        """Add a breadcrumb to the list.

        :param label: The breadcrumb label/text.
        :type label: str || unicode

        :param url: The URL or pattern name.
        :type url: str || unicode

        :param pattern_args: Pattern arguments when the URL is given as a pattern name.
        :type pattern_args: list

        :param pattern_kwargs: Pattern keyword arguments when the URL is given as a pattern name.
        :type pattern_kwargs: dict

        """
        if pattern_args or pattern_kwargs:
            url = reverse(url, args=pattern_args, kwargs=pattern_kwargs)

        breadcrumb = Breadcrumb(label, url)
        self.items.append(breadcrumb)


class Table(BaseHTML):
    """Represents an HTML table.

    .. code:: python

        # in your view ...
        table = Table()
        table.add_column("title", _("Project Title"))
        table.add_column("due_date", _("Due Date"))
        table.add_column("description", _("Description")

        qs = Projects.objects.all()
        for project in qs:
            table.add_row(project.title, project.due_date, project.description)

    """

    def __init__(self, **kwargs):
        self.caption = kwargs.pop("caption", None)
        self.is_striped = kwargs.pop("is_striped", False)
        self._attributes = kwargs
        self._columns = list()
        self._rows = list()

        super(Table, self).__init__(**kwargs)

    def add_column(self, name, title):
        """Add a column to the table.

        :param name: The field name.
        :type name: str

        :param title: The column heading.
        :type title: str

        """
        self._columns.append(TableColumn(name, title))

    def add_row(self, *args):
        """Add a row to the table."""
        self._rows.append(TableRow(*args))

    @property
    def columns(self):
        return self.get_columns()

    def get_columns(self):
        """Get columns.

        :rtype: list

        """
        return self._columns

    def get_rows(self):
        """Get rows.

        :rtype: list

        """
        return self._rows

    @property
    def rows(self):
        return self.get_rows()

    def to_html(self):
        a = list()

        attrs = flatatt(self.get_attributes())
        a.append('<table %s>' % attrs)

        if self.caption:
            a.append('<caption>%s</caption>' % self.caption)

        a.append('<thead>')
        for c in self.get_columns():
            a.append(c.to_html())
        a.append('</thead>')

        a.append('<tbody>')
        for r in self.get_rows():
            a.append(r.to_html())
        a.append('</tbody>')

        a.append('</table>')

        return "\n".join(a)


class TableColumn(BaseHTML):
    """Represents a table column."""

    def __init__(self, name, title, **kwargs):
        self.name = name
        self.title = title

        super(TableColumn, self).__init__(**kwargs)

        self._attributes['id'] = "table-column-%s" % name

    def __str__(self):
        return self.title

    def to_html(self):
        attrs = flatatt(self.get_attributes())
        return '<th %s>%s</th>' % (attrs, self.title)


class TableRow(BaseHTML):
    """Represents a row of data in a table."""

    def __init__(self, *args, **kwargs):
        """Initialize a table row.

        The data is pulled from the ``args``, while ``kwargs`` may be any valid row attribute:

        .. code-block:: python

            qs = Todo.objects.all()
            for r in qs:
                row = TableRow(
                    r.title,
                    r.due_dt,
                    r.description,
                )

        """
        self._data = args

        super(TableRow, self).__init__(**kwargs)

    @property
    def data(self):
        return self.get_data()

    def get_data(self):
        """Get the row data."""
        for d in self._data:
            yield d

    def to_html(self):
        attrs = flatatt(self.get_attributes())

        a = list()
        a.append('<tr %s>' % attrs)
        for data in self.get_data():
            return '<td %s>%s</td>' % (attrs, data)

        a.append('</tr>')

        return "\n".join(a)
