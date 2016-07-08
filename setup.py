#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import telegrambot

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = telegrambot.__version__

if sys.argv[-1] == 'publish':
    try:
        import wheel
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-telegram-bot',
    version="0.6.0",
    description="""Django app to write Telegram bots""",
    long_description=readme + '\n\n' + history,
    author='Juan Madurga',
    author_email='jlmadurga@gmail.com',
    url='https://github.com/jlmadurga/django-telegram-bot',
    packages=[
        'telegrambot',
    ],
    include_package_data=True,
    install_requires=[
        'django>=1.8.0',
        'python-telegram-bot==3.2.0',
        'djangorestframework==3.3.2',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-telegram-bot',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',        
    ],
)
