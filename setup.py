# coding: UTF-8
from distutils.core import setup
from os import path

"""
=====================
Flask-ReportableError
=====================

Introduction
------------

Flask-ReportableError is an Flask extension for handling errors that can
be reported to the web client.


Documentation
-------------

In order to use Flask-ReportableError, you must include the following
statement in you application start script::

    from flask import Flask
    import flask_reportable_error

    app = Flask(__name__)
    app.config.from_envvar('FLASK_SETTINGS', silent=True)
    flask_reportable_error.init(app)


API
---

- ``flask_reportable_error.reportable``:
  factory to create reportable exception classes. For example::

    raise reportable(ValueError)('invalid data received')


- ``flask_reportable_error.ReportableErrorMixin``:
  mixin for reportable exception classes.

  - ``report()``:
    method that returns the reportable string – can be overridden.

  - ``status_code``:
    property representing the numeric status code – can be set at
    instance level.


Settings
--------

The Flask settings may contain the key ``REPORTABLE_ERROR``, that’s a
dictionary with the following keys:

- ``LOGLEVEL``:
  the logging level. If not supplied, Flask-ReportableError uses
  ``logging.ERROR``.

- ``DEFAULT_STATUS_CODE``:
  the default numeric status code for reportable exception classes. By
  default is 500.
"""


setup(
    name             = 'flask_reportable_error',
    version          = '0.2.0',
    license          = 'BSD',
    platforms        = 'any',
    url              = 'https://github.com/Montegasppa/Flask-ReportableError',
    download_url     = 'https://github.com/Montegasppa/Flask-ReportableError/archive/master.zip',
    py_modules       = ['flask_reportable_error'],
    author           = 'Rodrigo Cacilhας',
    author_email     = 'batalema@cacilhas.info',
    description      = 'handle errors that can be reported to the web client',
    long_description = __doc__,
    install_requires = ['Flask>=0.10.1'],
    classifiers      = [
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
