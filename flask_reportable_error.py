# coding: UTF-8
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>
#                   Cesar Barros <cesarb@cesarb.eti.br>

import sys
from functools import wraps
from flask import render_template
try:
    from sqlalchemy.exc import DontWrapMixin
except ImportError:
    DontWrapMixin = object


__all__ = ['init', 'ReportableErrorMixin', 'reportable']


def init(app, template=None):
    config.update(app)
    config.template = template


@apply
class config(object):

    app = None

    def update(self, app):
        self.app = app

        @app.errorhandler(ReportableErrorMixin)
        def reportable_error_handler(exc):
            app.logger.log(self.loglevel, '(%s) %s', type(exc).__name__, exc)
            template = self.template
            body = render_template(template, { 'exc': exc }) if template \
              else exc.report()
            return body, exc.status_code, {}

    @property
    def settings(self):
        app = self.app
        if app is None:
            raise RuntimeError('you must run init() before using flask_reportable_error')
        return app.config.get('REPORTABLE_ERROR', {})

    @property
    def loglevel(self):
        import logging
        return self.settings.get('LOGLEVEL', logging.ERROR)

    @property
    def default_status_code(self):
        return self.settings.get('DEFAULT_STATUS_CODE', 500)


class ReportableErrorMixin(Exception, DontWrapMixin):

    _status_code = None

    def report(self):
        if sys.version_info.major == 3:
            return str(self)
        else:
            return unicode(self)

    @property
    def status_code(self):
        if self._status_code is None:
            return config.default_status_code
        else:
            return self._status_code

    @status_code.setter
    def status_code(self, value):
        self._status_code = value


def single_argument_memoize(f):
    memo = {}

    @wraps(f)
    def wrapper(arg):
        resp = memo.get(arg)
        if resp is None:
            resp = memo[arg] = f(arg)
        return resp

    return wrapper


@single_argument_memoize
def reportable(exception):
    if issubclass(exception, ReportableErrorMixin):
        return exception

    return type(
        'Reportable{0.__name__}'.format(exception),
        (exception, ReportableErrorMixin),
        {},
    )
