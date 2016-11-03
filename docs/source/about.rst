*****
About
*****

HTM Gel is a Django app for working with HTML in a generic and dynamic way.

Status
======

The API is changing at a rapid pace. Use at your own risk.

Install
=======

.. note::
    These instructions need to be tested.

To install:

.. code-block:: bash

    pip install https://github.com/bogeymin/django-htmgel/zipball/master;

Or in your requirements file:

.. code::

    -e git+https://github.com/bogeymin/django-htmgel/zipball/master#egg=htmgel

Or in your ``setup.py`` file:

.. code-block:: python

    install_requires=["htmgel"],
    dependency_links=[
        "https://github.com/bogeymin/django-htmgel/zipball/master",
    ]

Settings
========

Add the app to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'htmgel',
        ...
    ]

Define your framework:

.. code-block:: python

    HTML_FRAMEWORK = "bootstrap3"

.. note::
    ``bootstrap3`` is the only framework that is (sort of) fully supported at this time.

Documentation
=============

To generate the documentation, you need to ...

Install the additional requirements:

.. code-block:: bash

    pip install -r docs/requirements.pip;

Create a demo project:

.. code-block:: bash

    django-admin startproject demo;

Run the make:

.. code-block:: bash

    (cd docs && make html);

Open ``docs/build/index.html``.