"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from configparser import ConfigParser


def get_version():
    version = '0.5.0-default'
    if path.exists('app.ini'):
        config = ConfigParser()
        config.read('app.ini')
        version = config['version']['app_version']
    return version


setup(
    name='simpleweb',
    version=get_version(),
    description='A simple Python web project',
    author='Marc McKernan',
    author_email='marcmckernan@yahoo.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='sample setuptools development',
    packages=find_packages(),
    python_requires='>=3.5.*, <4',
    install_requires=['Flask',
                      'gunicorn',
                      'redis'],
    package_data={
        'app': ['templates/*.html'],
    }
)
