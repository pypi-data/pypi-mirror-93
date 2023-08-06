import os
import re

from setuptools import setup


def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    return [
        dirpath for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, '__init__.py'))
    ]


def get_requirements(path='.', extra='', default=None):
    path = os.path.join(os.path.abspath(path), f'requirements-{extra}.txt' if extra else 'requirements.txt')
    if not os.path.isfile(path):
        return default or []

    reqs = []
    with open(path) as reqs_txt:
        for package in reqs_txt:
            package = package.strip()
            if package and not package.startswith('#'):
                reqs.append(package)

    return reqs


setup(
    name='mxc',
    version=get_version('mxc'),
    url='https://github.com/propermx/mxc',
    license='MIT',
    description='ProperMX Command Line Interface (CLI)',
    author='ProperMX Team',
    author_email='dev@propermx.com',
    packages=get_packages('mxc'),
    install_requires=get_requirements(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'mxc = mxc.cli:run',
        ]
    }
)
