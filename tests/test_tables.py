# import mock
import unittest
from htmgel.library import Table

# Helpers


# Tests


class TestTable(unittest.TestCase):

    def setUp(self):
        self.data = [
            ("Mobile App", "2017-12-01", "2018-01-31", "active"),
            ("Website Project", "2017-11-01", "2017-12-31", "late"),
            ("Marketing Plan", "2018-01-01", "2018-01-31", "active"),
        ]

    def test_iter(self):
        """Check table iteration over rows."""
        t = Table(caption="Test Table", classes="table table-bordered", id="test-table")
        for d in self.data:
            t.add_row(d)

        count = 0
        for row in t:
            count += 1

        self.assertEqual(3, count)

    def test_add_column(self):
        """Check that table columns are properly added."""
        t = Table(caption="Test Table", classes="table table-bordered", id="test-table")
        t.add_column("project")
        t.add_column("start", title="Start Date")
        t.add_column("end", title="End Date")
        t.add_column("status")

        self.assertEqual(4, len(t.columns))

    def test_to_html(self):
        """Check HTML output."""
        t = Table(caption="Test Table", classes="table table-bordered", id="test-table")
        t.add_column("project")
        t.add_column("start", title="Start Date")
        t.add_column("end", title="End Date")
        t.add_column("status")

        for d in self.data:
            t.add_row(d)

        output = t.to_html()
        self.assertTrue("Website Project" in output)
