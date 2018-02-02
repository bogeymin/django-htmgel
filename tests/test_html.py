import unittest
from htmgel.library import BaseHTML, Link

# Tests


class TestBaseHTML(unittest.TestCase):

    def test_repr(self):
        """Check text representation of an element."""
        span = BaseHTML("testing")
        self.assertEqual("<BaseHTML span>", repr(span))

    def test_str(self):
        """Check string output of an element."""
        span = BaseHTML("testing")
        self.assertEqual("<span>testing</span>", str(span))

    def test_attributes(self):
        """Check HTML attributes."""
        span = BaseHTML("testing", classes="bold", id="myspan")

        self.assertEqual('class="bold" id="myspan"', span.attributes.strip())

        # self.assertEqual('<span class="bold" id="myspan">testing</span>', span.to_html())


class TestLink(unittest.TestCase):

    def test_to_html(self):
        """Check HTML output of link."""
        link = Link("http://example.com")

        self.assertEqual('<a href="http://example.com">http://example.com</a>', link.to_html())

        link = Link("http://example.com", text="Example")
        self.assertEqual('<a href="http://example.com">Example</a>', link.to_html())
