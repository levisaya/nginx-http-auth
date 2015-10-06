#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import io
from setuptools import setup
# from setuptools.command.test import test as TestCommand

with open('requirements.txt', 'r') as fh:
    dependencies = [l.strip() for l in fh]

# class PyTest(TestCommand):
#     def finalize_options(self):
#         TestCommand.finalize_options(self)
#         self.test_args = ['tests/']
#         self.test_suite = True
#
#     def run_tests(self):
#         # import here, cause outside the eggs aren't loaded
#         import pytest
#         errno = pytest.main(self.test_args)
#         sys.exit(errno)

setup(name='nginx_ldap_auth',
      version='0.1',
      description='Plugin-based authentication for NGINX.',
      author='Andy Levisay',
      author_email='levisaya@gmail.com',
      url='https://github.com/levisaya/nginx-http-auth',
      license='MIT',
      long_description=io.open('./docs/README.rst', 'r', encoding='utf-8').read(),
      platforms='any',
      zip_safe=False,
      # cmdclass={'test': PyTest},
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 1 - Planning',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3'],
      packages=['nginx_http_auth', 'nginx_http_auth.authorizers'],
      package_data={'nginx_http_auth': ['templates/*.html']},
      install_requires=dependencies
      )