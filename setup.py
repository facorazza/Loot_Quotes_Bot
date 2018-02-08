# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Loot_Quotes_Bot',
    version='1.0',
    description='Script per il calcolo delle quotazioni degli oggetti del gioco Loot Bot.',
    long_description=readme,
    author='Corazza Federico',
    author_email='@.com',
    url='https://github.com/Imperator26/Loot_Quotes_Bot',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
