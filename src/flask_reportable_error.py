# coding: UTF-8
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>
#                   Cesar Barros <cesar.barros@gmail.com>

import sys
from functools import wraps
import logging
try:
    from sqlalchemy.exc import DontWrapMixin
except ImportError:
    DontWrapMixin = object


__all__ = ['init', 'ReportableErrorMixin', 'reportable']


def init(app):
    ReportableErrorMixin.app = app

    @app.errorhandler(ReportableErrorMixin)
    def reportable_error_handler(exc):
        config = app.config.get('REPORTABLE_ERROR', {})
        loglevel = config.get('LOGLEVEL', logging.DEBUG)
        app.logger.log(loglevel, '(%s) %s', type(exc).__name__, exc)
        return exc.report(), exc.status_code, {}


class ReportableErrorMixin(Exception, DontWrapMixin):

    app = None
    _status_code = None

    def report(self):
        if sys.version_info.major == 3:
            return '{}'.format(self)
        else:
            return unicode(self)

    @property
    def status_code(self):
        if self._status_code is None:
            config = self.app.config.get('REPORTABLE_ERROR', {})
            return config.get('DEFAULT_STATUS_CODE', 500)
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
