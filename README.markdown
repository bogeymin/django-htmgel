# HTM Gel

An app for more easily working with HTML.

## Status

The API is changing at a rapid pace. Use at your own risk.

## Install

To install with Twitter Bootstrap 3:

    pip install htmgel[bootstrap3]; # TODO

To install with Twitter Bootstrap 4:

    pip install htmgel[bootstrap4]; # TODO
    
To install with Foundation 6:

    pip install htmgel[foundation6]; # TODO

> Note: These instructions need to be tested.

To install:

	pip install https://github.com/develmaycare/django-htmgel.git;

Or in your requirements file:

	git+https://github.com/develmaycare/django-htmgel.git

Or in your ``setup.py`` file:

	install_requires=["django-htmgel"],
	dependency_links=[
		"https://github.com/develmaycare/django-htmgel.git",
	]

## Settings

Add the app to your ``INSTALLED_APPS``:

	INSTALLED_APPS = [
		...
		'htmgel',
		...
	]

Define your framework:

	HTML_FRAMEWORK = "bootstrap3"
	
> Note: ``bootstrap3`` is the only framework that is (sort of) fully supported at this time.

``HTML_FRAMEWORK`` must appear in your context.

## Documentation

To generate the documentation, you need to ...

Install the additional requirements:

	pip install -r docs/requirements.pip;
	
Create a demo project:

	django-admin startproject demo;
	
Run the make:

	(cd docs && make html);

Open ``docs/build/index.html``.

## History

For those interested in a long read on the theories behind HTM Gel, we have prepared a
[history](docs/source/history.rst) of the prototyping and decisions that have led to the 
current version of the app.
