import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'sqlalchemy',
    'alembic',
    'py-moneyed',
]


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='pyStock',
    version='0.1.1',
    description='A stock market model for persistence using SQLAlchemy',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Office/Business :: Financial"
    ],
    author='Leonardo Lazzaro',
    author_email='lazzaroleonardo@gmail.com',
    url='www.lazzaroleonardo.com.ar',
    keywords='stock market model persistence',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=[
        'pytest',
    ],
    test_suite="tests",

)
