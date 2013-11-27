# -*- coding: utf-8 -*-
"""
Doctest runner for 'collective.recipe.sphinxbuilder'.
"""
__docformat__ = 'restructuredtext'

import doctest
import pkg_resources
import unittest
import re
import zc.buildout.tests
import zc.buildout.testing
from zope.testing import renormalizing


# 'Not found: xyz' setuptools message suppressor. Copied from zc.buildout.
not_found = (re.compile(r'Not found: [^\n]+/(\w|\.)+/\r?\n'), '')

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def get_dependent_dists(pkg):
    """Get list of eggs required by `pkg`.

    Recursively get a list of egg names required by `pkg`.
    """
    result = []
    distr = pkg_resources.get_distribution(pkg)
    for req in distr.requires():
        result.extend(get_dependent_dists(req))
    name = distr.project_name
    if name not in [
        # Packages that are made available by zc.buildout automatically.
        'setuptools', 'zc.buildout',
        ]:
        result.append(name)
    return result


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)

    # Install any eggs that should be available in the tests
    # (zc.buildout does not make them available automatically but sets up
    # an own site_packages).
    for p in get_dependent_dists('collective.recipe.sphinxbuilder[tests]'):
        zc.buildout.testing.install_develop(p, test)

def test_suite():
    suite = unittest.TestSuite((
        doctest.DocFileSuite(
            '../docs/usage.rst',
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
                not_found,
            ]),
        ),
    ))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
