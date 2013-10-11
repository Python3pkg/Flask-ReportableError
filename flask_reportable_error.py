# coding: UTF-8
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>
#                   Cesar Barros <cesarb@cesarb.eti.br>

import sys
from functools import wraps
from flask import render_template

__all__ = ['init', 'ReportableErrorMixin', 'reportable']


def init(app, template=None):
    config.update(app)
    config.template = template


def add_mixins(*mixins):
    config.add_mixins(*mixins)


#-----------------------------------------------------------------------
# settings object

@apply
class config(object):

    app = None
    mixins = set()

    def update(self, app):
        self.app = app
        self.add_mixins(ReportableErrorMixin)

        @app.errorhandler(ReportableErrorMixin)
        def reportable_error_handler(exc):
            app.logger.log(self.loglevel, '(%s) %s', type(exc).__name__, exc)

            template = self.template
            body = render_template(template, { 'exc': exc }) if template \
              else exc.report()

            headers = getattr(exc, 'headers', {})
            return body, exc.status_code, headers

    def add_mixins(self, *mixins):
        for mixin in mixins:
            self.mixins.add(mixin)

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


#-----------------------------------------------------------------------
# the mixin itself

class ReportableErrorMixin(Exception):

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


#-----------------------------------------------------------------------
# the factory

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
    base = config.mixins.copy()
    base.add(ReportableErrorMixin)
    if all(issubclass(exception, mixin) for mixin in config.mixins):
        return exception
    base.add(exception)
    return type('Reportable{0.__name__}'.format(exception),
                tuple(base), {})


#-----------------------------------------------------------------------
# SQLAlchemy support

try:
    from sqlalchemy.exc import DontWrapMixin
    add_mixins(DontWrapMixin)

except ImportError:
    # SQLAlchemy is not installed
    pass
