#!/usr/bin/env python

import setuptools 
with open('README.md') as f:
    readme = f.read()

setuptools.setup(name='sn-stat',
        version='0.2',
        description='Statistical methods for supernova neutrino detection',
        long_description=readme,
        long_description_content_type='text/markdown',
        url='https://github.com/Sheshuk/sn-stat',
        author='Andrey Sheshukov',
        author_email='ash@jinr.ru',
        licence='GNU GPLv3',
        packages=['sn_stat'],
        install_requires=['numpy','scipy']
     )

