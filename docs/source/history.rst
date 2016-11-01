******************************************
Rendering Common HTML Elements with Django
******************************************

One of the advantages of an HTML framework (such as Twitter Bootstrap and Zurb Foundation)
is the number of standard components that may be used "out of the box".

Since these components may be commonly used by Django apps or projects, it would make
sense to make them re-usable.

There are a number of possible approaches to this, but the general idea is to abstract the
components away from the template designer so that the framework may be interchangeable,
which increases the flexibility of themes and apps.

Tag, API, Renderer
==================

In this approach, the abstraction of standard components is handled entirely with program
code.

Implications
------------

Different frameworks have different components and different names for the same
components. A standard set of components and names must be established and mapped to the
appropriate component within each framework.

Approach
--------

Structure
.........

The structure of the app looks like this:

.. code::

	htmgel
	├── __init__.py
	├── api.py
	├── render
	│   ├── __init__.py
	│   └── bootstrap3
	│       ├── __init__.py
	│       ├── constants.py
	│       └── utils.py
	├── templatetags
	│   ├── __init__.py
	│   ├── htmgel_tags.py

Renderer
........

The renderer defines the functions needed to render the components:

.. code-block:: python

	# htmgel/render/bootstrap3/__init__.py
	def render_alert(content, display_type, dismissable=True, title=None):
		css_class = "alert alert-%s" % display_type
		if dismissable:
			css_class += " alert-dismissable"

		html = list()
		html.append('<div class="%s">' % css_class)

		if dismissable:
			html.append('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>')

		if title is not None:
			content = "<strong>%s</strong> %s" % (title, content)

		html.append(content)
		html.append('</div>')

		return "\n".join(html)

This requires one function for each component for each renderer.

API
...

The API loads the appropriate renderer and extracts the pre-defined functions.

.. code-block:: python

	# htmgel/api.py
	HTML_TAGS_RENDERER = getattr(settings, "HTML_TAGS_RENDERER", "htmgel.render.bootstrap3")
	TEMPLATE_DEBUG = getattr(settings, "TEMPLATE_DEBUG", False)

	try:
		renderer = import_module(HTML_TAGS_RENDERER)
	except ImportError:
		raise


	def raise_render_error(renderer, function_name):
		"""Raise an error when a given render function does not exist."""
		if TEMPLATE_DEBUG:
			raise AttributeError("%s function does not exist for the %s renderer." % (function_name, renderer))

	try:
		render_alert = getattr(renderer, "render_alert")
	except AttributeError:
		raise_render_error(renderer, "render_alert")

Tags
....

Tags import from the API and define wrapper functions.

.. code-block:: python

	# htmgel/templatetags/htmgel_tags.py
	@register.simple_tag
	def alert(*args, **kwargs):
		"""Return HTML for an alert.

		:param content: The content of the alert.
		:type content: str

		:param display_type: One of the VALID_DISPLAY_TYPES.
		:type dispaly_type: str

		:param dismissable: Indicates whether the should be able to dismiss the
						   alert. Defaults to ``True``.
		:type dismissable: bool

		:param title: If given, the title is prefixed to the content and enclosed
					  in a ``strong`` tag.
		:type title: str
		"""
		return render_alert(*args, **kwargs)

Templates
.........

The template loads and uses the tags.

.. code::

	# example.html
	{% extends "base.html" %}
	{% load htmgel_tags %}

	{% block content %}
		{% if error_message %}
			{% alert error_message "error" dismissable=True title="Error" %}
		{% endif %}
	{% endblock %}

Observations
------------

- The architecture is confusing and hard to follow.
- It is difficult to remember the function signatures of the tags, and especially which ones are required and which ones are optional.
- This is approach is clever, but not necessarily good.

Template Loader
===============

This approach uses a template loader to dynamically select the proper template.

Implications
------------

Non-standard settings must be used.

Approach
--------

Structure
.........

The app is structured like so:

.. code::

	htmgel
	├── __init__.py
	├── loaders.py
	└── templates
		└── htmgel
			├── bootstrap3
			│   └── alert.html
			└── foundation6
				└── alert.html

Settings
........

Template settings need to include ``loaders`` in the ``OPTIONS``.

.. code-block:: python

	TEMPLATES = [
		{
			'BACKEND': 'django.template.backends.django.DjangoTemplates',
			'DIRS': [
				os.path.join(BASE_DIR, "theme"),
				os.path.join(BASE_DIR, "main", "templates"),
				os.path.join(BASE_DIR, ".."),  # assuming apps are stored above main/
			],
			'APP_DIRS': True,
			'OPTIONS': {
				'context_processors': [
					'django.template.context_processors.debug',
					'django.template.context_processors.request',
					'django.contrib.auth.context_processors.auth',
					'django.contrib.messages.context_processors.messages',
				],
				'loaders': [
					'htmgel.loaders.Loader',
					'django.template.loaders.filesystem.Loader',
					'django.template.loaders.app_directories.Loader',
				],
			},
		},
	]

	HTML_FRAMEWORK = "foundation6"

Loader
......

The loader looks for ``htmgel`` and sends back the template based on the selected HTML
framework.

.. code-block:: python

	# htmgel.loaders.py
	import os
	from django.conf import settings
	from django.template import TemplateDoesNotExist
	from django.template.base import Origin
	from django.template.loaders.base import Loader as BaseLoader

	HTML_FRAMEWORK = getattr(settings, "HTML_FRAMEWORK", "bootstrap3")


	class Loader(BaseLoader):

		def get_contents(self, origin):

			try:
				with open(origin.name, "rb") as f:
					contents = f.read()
					f.close()
					return contents
			except IOError:
				raise TemplateDoesNotExist(origin.name)

		def get_template_sources(self, template_name):
			if "htmgel" in template_name:
				include = template_name.split("/")[1]
				path = os.path.join("htmgel", "templates", "htmgel", HTML_FRAMEWORK, include)
				yield Origin(path, template_name)

Templates
.........

The template uses an include, but the template loader interprets the request.

.. code::

	# example.html
	{% extends "base.html" %}

	{% block content %}
		{% if error_message %}
			{% include "htmgel/alert.html" with title="Error" message=error_message %}
		{% endif %}
	{% endblock %}

Observations
------------

- This works because the custom template loader intercepts and "corrects" includes for a
  a sub-template that does not exist, replacing it with one from the selected framework.
- ``get_template_sources()`` normally returns a number of possible locations, while our
  example only returns one. This may not be an issue.
- This approach feels clever, but brittle. Perhaps it is not brittle at all, but it does
  require additional template-related settings beyond the default.

Dynamic Include
===============

This approach makes use of standard Django includes to load HTML components.

Implications
------------

Use of ``include`` prohibits the use of other template engines, which makes themes and
apps less flexible.

Approach
--------

Settings
........

The settings include:

.. code-block:: python

    HTML_FRAMEWORK = "foundation6"

    SETTINGS_IN_CONTEXT = [
        "HTML_FRAMEWORK",
    ]

We've included a context processor called ``settings_in_context`` which puts the
``HTML_FRAMEWORK`` setting in the request context.

.. code-block:: python

	TEMPLATES = [
		{
			'BACKEND': 'django.template.backends.django.DjangoTemplates',
			'DIRS': [
				os.path.join(BASE_DIR, "theme"),
				os.path.join(BASE_DIR, "main", "templates"),
				os.path.join(BASE_DIR, ".."),  # assuming apps are stored above main/
			],
			'APP_DIRS': True,
			'OPTIONS': {
				'context_processors': [
					'django.template.context_processors.debug',
					'django.template.context_processors.request',
					'django.contrib.auth.context_processors.auth',
					'django.contrib.messages.context_processors.messages',
				],
			},
		},
	]

Structure
.........

The app is structured like so:

.. code::

	htmgel
	├── __init__.py
	└── templates
		└── htmgel
			├── alert.html
			├── bootstrap3
			│   └── alert.html
			└── foundation6
				└── alert.html

The top-level ``alert.html`` looks at the ``HTML_FRAMEWORK`` setting:

.. code::

	# htmgel/templates/htmgel/alert.html
	{% if HTML_FRAMEWORK == "bootstrap3" %}
    	{% include "htmgel/bootstrap3/alert.html" %}
	{% elif HTML_FRAMEWORK == "foundation6" %}
		{% include "htmgel/foundation6/alert.html" %}
	{% else %}
		<p class="alert"><b>{{ title }}</b> {{ message }}</p>
	{% endif %}

Templates
.........

The template uses an include and the conditionals handle the rest.

.. code::

	# example.html
	{% extends "base.html" %}

	{% block content %}
		{% if error_message %}
			{% include "htmgel/alert.html" with title="Error" message=error_message %}
		{% endif %}
	{% endblock %}

Observations
------------

- This relies on standard Django functionality which means apps or projects *could*
  override these templates if needed.
- An additional template must be maintained for each component, and these templates must
  be updated whenever a new framework is added.
- The number of templates required does not change compared to the other approaches.
- It is possible to define default output in the event that the framework does not support
  the component.

Compare and Contrast
====================

Each of these approaches work, and each have advantages and disadvantages. The most simple
and straight forward is the Dynamic Include.

There is no substantial difference between ...

.. code::

	{% alert error_message "error" dismissable=True title="Error" %}

and ...

.. code::

	{% include "htmgel/alert.html" with title="Error" message=error_message %}

Except that the first approach requires a great deal of supporting code.

Additionally, the Template Loader approach simply adds additional code without improving
the functionality. It *does* improve the maintainability slightly, but not by much.

Conclusion
----------

After trying each of the approaches, we decided to use the Dynamic Include for HTML Gel.
It is comparatively simple, keeps HTML where it belongs, and requires very little program
code.
