import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'sqlalchemy',
    'alembic',
    'psycopg2'
]

setup(
    name='pyStock',
    version='0.0.8',
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
    tests_require=requires,
    test_suite="pyStock",
)
