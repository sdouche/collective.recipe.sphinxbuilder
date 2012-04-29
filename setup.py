# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.recipe.sphinxbuilder
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.7.1'
sphinx_version = '>=1.0'

long_description = (
    read('README.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('src', 'collective', 'recipe', 'sphinxbuilder', 'docs', 'about_sphinx.txt')
    + '\n' +
    read('src', 'collective', 'recipe', 'sphinxbuilder', 'docs', 'quick_start.txt')
    + '\n' +
    read('src', 'collective', 'recipe', 'sphinxbuilder', 'docs', 'options.txt')
    + '\n' +
    read('src', 'collective', 'recipe', 'sphinxbuilder', 'docs', 'usage.txt')
    + '\n' +
    read('src', 'collective', 'recipe', 'sphinxbuilder', 'docs', 'contributors.txt')
    + '\n' +
    read('src', 'collective', 'recipe', 'sphinxbuilder', 'docs', 'history.txt')
    )




setup(name='collective.recipe.sphinxbuilder',
      version=version,
      description="ZC.buildout recipe to generate and build Sphinx-based documentation in the buildout.",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Zope Public License',
        ],
      keywords='buildout sphinx',
      author='Tarek Ziade',
      author_email='tarek@ziade.org',
      url='https://github.com/sdouche/collective.recipe.sphinxbuilder',
      license='ZPL',
      packages = find_packages('src', exclude=['ez_setup']),
      package_dir = {'':'src'},
      namespace_packages=['collective', 'collective.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'setuptools',
            'zc.buildout',
            'zc.recipe.egg',
            'docutils',
            'Sphinx'+sphinx_version],
      tests_require=['zope.testing', 'zc.buildout'],
      extras_require=dict(tests=['zope.testing', 'zc.buildout']),
      test_suite = 'collective.recipe.sphinxbuilder.tests.test_docs.test_suite',
      entry_points = {"zc.buildout": ["default = collective.recipe.sphinxbuilder:Recipe"]}
      )

# python setup.py --long-description | rst2html.py > /dev/null
