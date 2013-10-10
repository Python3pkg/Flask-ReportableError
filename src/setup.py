# coding: UTF-8
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>

from distutils.core import setup


setup(
    name         = 'flask_reportable_error',
    version      = '0.1.0',
    licence      = 'BSD',
    platforms    = 'any',
    py_modules   = ['flask_reportable_error'],
    author       = 'Rodrigo Cacilhας',
    author_email = 'batalema@cacilhas.info',
    description  = 'handle errors that can be reported to the web client',
    install_requires = [
        'Flask>=0.10.1',
    ],
    classifiers = [
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
