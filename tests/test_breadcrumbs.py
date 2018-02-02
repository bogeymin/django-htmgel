# import mock
import unittest
from htmgel.library import Breadcrumb, Breadcrumbs

# Helpers


# Tests


class TestBreadcrumb(unittest.TestCase):

    def test_get_absolute_url(self):
        """Check the output of the absolute URL."""
        b = Breadcrumb("Example", "/")
        self.assertEqual("/", b.get_absolute_url())

    def test_repr(self):
        """Check text representation of a breadcrumb."""
        b = Breadcrumb("Example", "/")
        self.assertEqual("<Breadcrumb Example>", repr(b))


class TestBreadcrumbs(unittest.TestCase):

    def test_iter(self):
        """Check iteration over breadcrumb items."""
        crumbs = Breadcrumbs()
        crumbs.add("Home", "/")
        crumbs.add("About Us", "/about/")
        crumbs.add("Contact", "/contact/")

        self.assertEqual(3, len(crumbs.items))

        count = 0
        for i in crumbs:
            count += 1

        self.assertEqual(3, count)

    # Can't test without django project and settings.
    # def test_add(self):
    #     """Check adding a breadcrumb from a pattern."""
    #     with mock.patch("django.urls.base.reverse", return_value="projects/detail/1"):
    #         crumbs = Breadcrumbs()
    #         crumbs.add("Test Project", "project_detail", pattern_args=[1])
    #
    #         self.assertEqual("projects/detail/1", crumbs.items[0].url)
