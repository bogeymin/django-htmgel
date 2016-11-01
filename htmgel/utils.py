

class Table(object):
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

    def __init__(self, border=None, caption=None, is_striped=None):
        self.border = border
        self.caption = caption
        self.is_striped = is_striped
        self._columns = list()
        self._rows = list()

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


class TableColumn(object):
    """Represents a table column."""

    def __init__(self, name, title):
        self.name = name
        self.title = title

    def __str__(self):
        return self.title


class TableRow(object):
    """Represents a row of data in a table."""

    def __init__(self, *args):
        self._data = args

    @property
    def data(self):
        return self.get_data()

    def get_data(self):
        """Get the row data."""
        for d in self._data:
            yield d
