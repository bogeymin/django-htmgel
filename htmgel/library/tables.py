# Imports

from django.utils.safestring import mark_safe
from .html import BaseHTML

# Classes


class Column(BaseHTML):
    """A column (header) in an HTML table."""

    def __init__(self, name, title=None, **kwargs):
        if title is not None:
            content = title
        else:
            content = name

        super(Column, self).__init__(content, **kwargs)

        self.name = name
        self._open_tag = "th"


class Row(BaseHTML):
    """A row in an HTML table."""

    def __init__(self, data, **kwargs):
        super(Row, self).__init__(data, **kwargs)
        self._open_tag = "tr"

    @mark_safe
    def to_html(self):
        a = list()
        a.append("<%s>" % self.get_open_tag())
        for d in self.content:
            a.append("<td>%s</td>" % d)

        a.append("</%s>" % self.get_close_tag())

        return "\n".join(a)


class Table(BaseHTML):
    """An HTML table."""

    def __init__(self, caption=None, columns=None, rows=None, **kwargs):
        super(Table, self).__init__("", **kwargs)
        self.caption = caption
        self.columns = columns or list()
        self.rows = rows or list()
        self._open_tag = "table"

    def __iter__(self):
        return iter(self.rows)

    def add_column(self, name, title=None, **kwargs):
        column = Column(name, title=title, **kwargs)
        self.columns.append(column)

        return column

    def add_row(self, data, **kwargs):
        row = Row(data, **kwargs)
        self.rows.append(row)

        return row

    @mark_safe
    def to_html(self):
        a = list()
        a.append("<%s>" % self.get_open_tag())

        if self.caption is not None:
            caption = BaseHTML(self.caption, open_tag="caption")
            a.append(caption.to_html())

        a.append("<thead><tr>")
        for column in self.columns:
            a.append(column.to_html())
        a.append("</tr></thead>")

        a.append("<tbody>")

        for row in self.rows:
            a.append(row.to_html())

        a.append("</tbody>")

        a.append("</%s>" % self.get_close_tag())

        return "\n".join(a)


class QuerysetTable(Table):

    def __init__(self, queryset, caption=None, columns=None, rows=None, **kwargs):
        super(QuerysetTable, self).__init__(caption=caption, columns=columns, rows=rows, **kwargs)

        self.is_loaded = False
        self.queryset = queryset

    def __iter__(self):
        if not self.is_loaded:
            self.load()

        return iter(self.rows)

    def load(self):
        """Load data from queryset into ``rows``."""
        for record in self.queryset:
            data = list()
            for c in self.columns:
                try:
                    value = getattr(record, c.name)
                except AttributeError:
                    value = None

                data.append(value)

        self.is_loaded = True
