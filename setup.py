#!/usr/bin/env python

from distutils.core import setup

setup(name='Monasca-Alarm-Cleaner',
      version='1.1',
      description='Monasca Alarm Cleaner tool',
      author='Adam Hamsik',
      author_email='haaaad@gmail.com',
      url='https://github.com/Chillisystems/monasca-alarm-cleaner',
      packages=['MonascaCleaner'],
      scripts=['monasca-alarm-cleaner.py'],
      install_requires=[
          'python-monascaclient>=1.12',
          'openstacksdk>=0.19.0',
          'osc-lib>=1.11'
      ]
     )

