# Imports

from django.urls import reverse

# Exports

__all__ = (
    "Breadcrumb",
    "Breadcrumbs",
)

# Classes


class Breadcrumb(object):
    """Helper class that ensures an object has the required attributes."""

    def __init__(self, text, url):
        self.text = text
        self.url = url

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.text)

    def get_absolute_url(self):
        return self.url


class Breadcrumbs(object):
    """Collect objects to be displayed as breadcrumbs."""

    def __init__(self):
        self.items = list()

    def __iter__(self):
        return iter(self.items)

    def add(self, text, url, pattern_args=None, pattern_kwargs=None, namespace=None):
        """Add a breadcrumb to the list.

        :param text: The breadcrumb label/text.
        :type text: str

        :param url: The URL or pattern name.
        :type url: str

        :param pattern_args: Pattern arguments when the URL is given as a pattern name.
        :type pattern_args: list

        :param pattern_kwargs: Pattern keyword arguments when the URL is given as a pattern name.
        :type pattern_kwargs: dict

        :param namespace: The application namespace for the URL when given as a pattern name.
        :type namespace: str

        :rtype: Breadcrumb

        """
        if pattern_args or pattern_kwargs:
            if namespace is not None:
                _url = "%s:%s" % (namespace, url)
            else:
                _url = url

            actual_url = reverse(_url, args=pattern_args, kwargs=pattern_kwargs)
        else:
            actual_url = url

        breadcrumb = Breadcrumb(text, actual_url)
        self.items.append(breadcrumb)

        return breadcrumb
