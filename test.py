#!/usr/bin/env python
# coding: UTF-8
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>
#                   Cesar Barros <cesarb@cesarb.eti.br>

import logging
from unittest import main, TestCase
from mock import patch
import flask_reportable_error


class TestInit(TestCase):

    class Application(object):

        def __init__(self):
            self.handlers = {}
            self.config = {}
            self.logged = []
            self.logger = type('Logger', (object, ), {
                'log': lambda logger, *args: self.logged.append(args),
            })()

        def errorhandler(self, exc):
            def register(callback):
                self.handlers[exc] = callback
            return register

    def setUp(self):
        cls = type(self)
        app = self.app = cls.Application()
        flask_reportable_error.init(app)
        self.handler = app.handlers[
            flask_reportable_error.ReportableErrorMixin
        ]

    def test_custom_headers(self):
        exc = flask_reportable_error.reportable(ValueError)('some value error')
        exc.headers = { 'Content-Type': 'plain/text' }
        report, status_code, headers = self.handler(exc)
        self.assertEqual(headers, { 'Content-Type': 'plain/text' })

    @patch.object(flask_reportable_error, 'render_template')
    def test_handle_template(self, render_template):
        app = self.app
        flask_reportable_error.init(app, 'application/error.html')
        exc = flask_reportable_error.reportable(ValueError)('some value error')
        body, status_code, headers = self.handler(exc)
        render_template.assert_called_once_with(
            'application/error.html', { 'exc': exc })
        self.assertEqual(body, render_template.return_value)

    def test_raises_on_none_app(self):
        # Reset flask_reportable_error
        flask_reportable_error.config.app = None
        self.assertRaises(RuntimeError,
                          lambda: flask_reportable_error.config.settings)

    def test_register_application(self):
        self.assertEqual(self.handler.__name__,
                         'reportable_error_handler')
        self.assertEqual(flask_reportable_error.config.app,
                         self.app)

    def test_handle_error_500(self):
        s = 'test reportable error'
        exc = flask_reportable_error.ReportableErrorMixin(s)
        report, status_code, headers = self.handler(exc)
        self.assertEqual(report, s)
        self.assertEqual(status_code, 500)
        self.assertEqual(headers, {})

    def test_log_error(self):
        s = 'test reportable error'
        exc = flask_reportable_error.ReportableErrorMixin(s)
        self.handler(exc)
        self.assertEqual(self.app.logged, [
            (logging.ERROR, '(%s) %s', 'ReportableErrorMixin', exc),
        ])

    def test_inhibit_log(self):
        s = 'test reportable error'
        app = self.app
        app.config['REPORTABLE_ERROR'] = {
            'LOGLEVEL': logging.DEBUG,
        }
        exc = flask_reportable_error.ReportableErrorMixin(s)
        self.handler(exc)
        self.assertEqual(app.logged, [
            (logging.DEBUG, '(%s) %s', 'ReportableErrorMixin', exc),
        ])

    def test_handle_error_400(self):
        s = 'test reportable error'
        self.app.config['REPORTABLE_ERROR'] = {
            'DEFAULT_STATUS_CODE': 400,
        }
        exc = flask_reportable_error.ReportableErrorMixin(s)
        report, status_code, headers = self.handler(exc)
        self.assertEqual(report, s)
        self.assertEqual(status_code, 400)
        self.assertEqual(headers, {})

    def test_handle_own_status(self):
        s = 'test reportable error'
        exc = flask_reportable_error.ReportableErrorMixin(s)
        exc.status_code = 404
        report, status_code, headers = self.handler(exc)
        self.assertEqual(report, s)
        self.assertEqual(status_code, 404)
        self.assertEqual(headers, {})


class TestReportableErrorMixin(TestCase):

    def test_reportable_error_report(self):
        s = 'test reportable error'
        exc = flask_reportable_error.ReportableErrorMixin(s)
        self.assertEqual(exc.report(), s)

    def test_reportable_factory_return_reportable_error(self):
        exc_class = flask_reportable_error.reportable(ValueError)
        self.assertTrue(issubclass(exc_class,
                                   flask_reportable_error.ReportableErrorMixin))
        self.assertTrue(issubclass(exc_class, ValueError))

    def test_reportable_factory_response_report_error(self):
        s = 'test reportable error'
        exc = flask_reportable_error.reportable(ValueError)(s)
        self.assertEqual(exc.report(), s)

    def test_reportable_factory_response_be_memoized(self):
        exc1 = flask_reportable_error.reportable(ValueError)
        exc2 = flask_reportable_error.reportable(ValueError)
        exc3 = flask_reportable_error.reportable(AttributeError)
        self.assertIs(exc1, exc2)
        self.assertNotEqual(exc1, exc3)


class TestAddMixins(TestCase):

    def test_add_mixins(self):
        class Mixin(object):
            pass

        flask_reportable_error.add_mixins(Mixin)
        exc_class = flask_reportable_error.reportable(ValueError)
        self.assertTrue(issubclass(exc_class, Mixin))
        self.assertTrue(issubclass(exc_class, ValueError))
        self.assertTrue(issubclass(exc_class,
                                   flask_reportable_error.ReportableErrorMixin))


if __name__ == '__main__':
    main()
