#!/bin/env python3

from setuptools import find_packages, setup


def readme():
    with open('README.rst') as rdm:
        return rdm.read()


setup(name='jeri',
      version='0.1.0',
      description=(
          'A model based REST client framework'
      ),
      long_description=readme(),
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
      ],
      install_requires=[
          'requests',
      ],
      keywords='rest framework json',
      url='http://github.com/fmorgner/jeri.git',
      author='Felix Morgner',
      author_email='felix.morgner@gmail.com',
      license='BSD',
      include_package_data=True,
      packages=find_packages())
