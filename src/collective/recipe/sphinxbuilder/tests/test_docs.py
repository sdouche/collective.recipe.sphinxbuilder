# -*- coding: utf-8 -*-
"""
Doctest runner for 'collective.recipe.sphinxbuilder'.
"""
__docformat__ = 'restructuredtext'

import unittest
import zc.buildout.tests
import zc.buildout.testing

from zope.testing import doctest, renormalizing

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)

    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('collective.recipe.sphinxbuilder', test)

    # Install any other recipes that should be available in the tests
    for p in ['Sphinx==0.6.3', 'zc.recipe.egg', 'Jinja2>=2.1', 'Pygments>=0.8',
              'docutils>=0.4']:
        # TODO :: dont know why install methos is not working
        # upper recipes are not found in path
        zc.buildout.testing.install_develop(p, test)


def test_suite():
    suite = unittest.TestSuite((
            doctest.DocFileSuite(
                '../docs/usage.txt',
                setUp=setUp,
                tearDown=zc.buildout.testing.buildoutTearDown,
                optionflags=optionflags,
                checker=renormalizing.RENormalizing([
                        # If want to clean up the doctest output you
                        # can register additional regexp normalizers
                        # here. The format is a two-tuple with the RE
                        # as the first item and the replacement as the
                        # second item, e.g.
                        # (re.compile('my-[rR]eg[eE]ps'), 'my-regexps')
                        zc.buildout.testing.normalize_path,
                        ]),
                ),
            ))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
