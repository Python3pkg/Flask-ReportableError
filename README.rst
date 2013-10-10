=====================
Flask-ReportableError
=====================

Introduction
------------

Flask-ReportableError is a Flask extension for handling errors that can
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
  default it’s 500.
