from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


def read(filename):
    with open(filename) as f:
        return f.read()

setup(
    name='Henson-Sentry',
    version='0.4.0',
    author='Andy Dirnberger, Leonard Bedner, and others',
    author_email='henson@iheart.com',
    url='https://henson-sentry.readthedocs.io',
    description='A library for integrating Sentry into a Henson application',
    long_description=read('README.rst'),
    license='MIT',
    py_modules=['henson_sentry'],
    zip_safe=False,
    install_requires=[
        'Henson',
        'raven-aiohttp',
    ],
    tests_require=[
        'pytest',
        'pytest-asyncio',
    ],
    cmdclass={
        'test': PyTest,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
    ]
)
