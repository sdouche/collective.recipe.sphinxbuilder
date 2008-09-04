Supported options
=================

The recipe supports the following options:

autobuild
    If `autobuild` is set to `true`, the Sphinx documentation is generated
    automatically when buildout is relaunch. Otherwise it is a manual
    action by the user. Defaults to `false`.

doc-directory
    Specify the documentation root. Default to `docs`.    

doc-outputs
    Multiple-line value that defines what kind of output to produce. 
    Can be `html`, `latex` or `pdf`. Defaults to `html`.

Example usage
=============

The recipe can be used without any options. We'll start by creating a 
buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = sphinx
    ...
    ... [sphinx]
    ... recipe = collective.recipe.sphinxbuilder
    ... """) 

Let's run the buildout::

    >>> print 'start', system(buildout) 
    start...
    Installing sphinx.
    <BLANKLINE>

What are we expecting ? 

- a `docs` folder with a Sphinx structure.
- a script in the `bin` folder to build the docs.

    >>> docs = join(sample_buildout, 'docs')
    >>> ls(docs)
    - Makefile
    d source

    >>> source = join(docs, 'source')
    >>> ls(source) 
    d  _static
    d  _templates
    -  conf.py
    -  index.txt

