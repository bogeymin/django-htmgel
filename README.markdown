# HTM Gel

An app for working with HTML.

## Status

The API is changing at a rapid pace. Use at your own risk.

## Install

> Note: These instructions need to be tested.

To install:

	pip install https://github.com/bogeymin/htmgel/zipball/master;

Or in your requirements file:

	-e git+https://github.com/bogeymin/htmgel/zipball/master#egg=htmgel

Or in your ``setup.py`` file:

	install_requires=["htmgel"],
	dependency_links=[
		"https://github.com/bogeymin/htmgel/zipball/master",
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
	
> Note: ``bootstrap3`` is the only framework that is (sort of) fully supported at this 
> time.

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
