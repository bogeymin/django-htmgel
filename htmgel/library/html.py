# Imports

from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

# Exports

__all__ = (
    "BaseHTML",
    "Link",
)

# Classes


class BaseHTML(object):
    """Base class for HTML elements."""

    def __init__(self, content, close_tag=None, open_tag=None, **kwargs):
        self.content = content
        self._close_tag = close_tag
        self._open_tag = open_tag or "span"

        classes = kwargs.pop("classes", None)
        if classes is not None:
            kwargs['class'] = classes

        self._attributes = kwargs

    def __repr__(self):
        return "<%s %s%s>" % (self.__class__.__name__, self._open_tag, flatatt(self._attributes))

    def __str__(self):
        return self.to_html()

    @property
    def attributes(self):
        """Get the flattened attributes for the element.

        :rtype: str

        """
        return flatatt(self._attributes)

    def get_close_tag(self):
        """Get the closing tag for the element.

        :rtype: str

        """
        return self._close_tag or self._open_tag

    def get_open_tag(self):
        """Get the opening tag for the element.

        :rtype: str

        """
        return "%s%s" % (self._open_tag, flatatt(self._attributes))

    @mark_safe
    def to_html(self):
        # if isinstance(self.content, (list, tuple)):
        #     content = "\n".join(self.content)
        # else:
        #     content = self.content

        return "<%s>%s</%s>" % (self.get_open_tag(), self.content, self.get_close_tag())


class Link(BaseHTML):
    """An HTML link."""

    def __init__(self, href, text=None, **kwargs):
        if text is not None:
            content = text
        else:
            content = href

        kwargs['href'] = href

        super(Link, self).__init__(content, open_tag="a", **kwargs)
