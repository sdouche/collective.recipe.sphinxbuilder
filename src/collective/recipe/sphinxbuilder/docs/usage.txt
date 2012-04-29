=============
Example usage
=============

The recipe can be used without any options. We'll start by creating a
buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = sphinxbuilder
    ...
    ... [sphinxbuilder]
    ... recipe = collective.recipe.sphinxbuilder
    ... source = collective.recipe.sphinxbuilder:docs
    ... """)

Let's run the buildout::

    >>> print 'start', system(buildout)
    start Installing sphinxbuilder.
    collective.recipe.sphinxbuilder: writing MAKEFILE..
    collective.recipe.sphinxbuilder: writing BATCHFILE..
    collective.recipe.sphinxbuilder: writing custom sphinx-builder script..
    Generated script '/sample-buildout/bin/sphinx-quickstart'.
    Generated script '/sample-buildout/bin/sphinx-build'.
    <BLANKLINE>

What are we expecting?

A `docs` folder with a Sphinx structure::

    >>> docs = join(sample_buildout, 'docs')
    >>> ls(docs)
    - Makefile
    -  make.bat

A script in the `bin` folder to build the docs::

    >>> bin = join(sample_buildout, 'bin')
    >>> ls(bin)
    - buildout
    - sphinx-build
    - sphinx-quickstart
    - sphinxbuilder

The content of the script is a simple shell script::

    >>> script = join(sample_buildout, 'bin', 'sphinxbuilder')
    >>> print open(script).read()
    cd ...docs
    make html

    >>> print 'start', system(script)
    start /sample-buildout/bin/sphinx-build -b html -d /sample-buildout/docs/doctrees ...src/collective/recipe/sphinxbuilder/docs /sample-buildout/docs/html
    ...

If we want `latex`, we need to explicitly define it::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = sphinxbuilder
    ...
    ... [sphinxbuilder]
    ... recipe = collective.recipe.sphinxbuilder
    ... source = collective.recipe.sphinxbuilder:docs
    ... outputs =
    ...     html
    ...     latex
    ... """)
    >>> print 'start', system(buildout)
    start Uninstalling sphinxbuilder.
    Installing sphinxbuilder.
    collective.recipe.sphinxbuilder: writing MAKEFILE..
    collective.recipe.sphinxbuilder: writing BATCHFILE..
    collective.recipe.sphinxbuilder: writing custom sphinx-builder script..
    <BLANKLINE>

Let's see our script now::

    >>> cat(script)
    cd ...docs
    make html
    make latex

Finally let's run it::

    >>> print 'start', system(script)
    start /sample-buildout/bin/sphinx-build -b html -d /sample-buildout/docs/doctrees   .../src/collective/recipe/sphinxbuilder/docs /sample-buildout/docs/html
    ...
    <BLANKLINE>
    Build finished. The HTML pages are in /sample-buildout/docs/html.
    ...
    Build finished; the LaTeX files are in /sample-buildout/docs/latex.
    Run `make' in that directory to run these through (pdf)latex...
    Making output directory...
    <BLANKLINE>

If we want `pdf`, we need to explicitly define it::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = sphinxbuilder
    ...
    ... [sphinxbuilder]
    ... recipe = collective.recipe.sphinxbuilder
    ... source = collective.recipe.sphinxbuilder:docs
    ... outputs =
    ...     html
    ...     latex
    ...     pdf
    ... """)
    >>> print 'start', system(buildout)
    start Uninstalling sphinxbuilder.
    Installing sphinxbuilder.
    collective.recipe.sphinxbuilder: writing MAKEFILE..
    collective.recipe.sphinxbuilder: writing BATCHFILE..
    collective.recipe.sphinxbuilder: writing custom sphinx-builder script..
    <BLANKLINE>

Let's see our script now::

    >>> cat(script)
    cd ...docs
    make html
    make latex
    cd /sample-buildout/docs/latex && make all-pdf

We will skip running the script in tests, because the PDF builder depends
on libraries which may not be installed.

If we want `epub`, like pdf we need to explicitly define it::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = sphinxbuilder
    ...
    ... [sphinxbuilder]
    ... recipe = collective.recipe.sphinxbuilder
    ... source = collective.recipe.sphinxbuilder:docs
    ... outputs =
    ...     html
    ...     epub
    ... """)
    >>> print 'start', system(buildout)
    start Uninstalling sphinxbuilder.
    Installing sphinxbuilder.
    collective.recipe.sphinxbuilder: writing MAKEFILE..
    collective.recipe.sphinxbuilder: writing BATCHFILE..
    collective.recipe.sphinxbuilder: writing custom sphinx-builder script..
    <BLANKLINE>

Let's see our script now::

    >>> cat(script)
    cd ...docs
    make html
    make epub

We can also have the script run any doctests in the docs while building::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = sphinxbuilder
    ...
    ... [sphinxbuilder]
    ... recipe = collective.recipe.sphinxbuilder
    ... source = collective.recipe.sphinxbuilder:docs
    ... outputs =
    ...     doctest
    ...     html
    ... """)
    >>> print 'start', system(buildout)
    start Uninstalling sphinxbuilder.
    Installing sphinxbuilder.
    collective.recipe.sphinxbuilder: writing MAKEFILE..
    collective.recipe.sphinxbuilder: writing BATCHFILE..
    collective.recipe.sphinxbuilder: writing custom sphinx-builder script..
    <BLANKLINE>

Let's see our script now::

    >>> cat(script)
    cd ...docs
    make doctest
    make html

Again, we will skip running them, this time to avoid a recursive fork bomb. ;)

If we want `extra-paths`, we can define them as normal paths or as unix
wildcards (see `fnmatch` module) ::
    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = sphinxbuilder
    ...
    ... [sphinxbuilder]
    ... recipe = collective.recipe.sphinxbuilder
    ... source = collective.recipe.sphinxbuilder:docs
    ... extra-paths =
    ...     develop-eggs/
    ...     eggs/*
    ... """)
    >>> print 'start', system(buildout)
    start Uninstalling sphinxbuilder.
    Installing sphinxbuilder.
    collective.recipe.sphinxbuilder: writing MAKEFILE..
    collective.recipe.sphinxbuilder: writing BATCHFILE..
    collective.recipe.sphinxbuilder: writing custom sphinx-builder script..
    collective.recipe.sphinxbuilder: inserting extra-paths..
    Generated script '/sample-buildout/bin/sphinx-quickstart'.
    Generated script '/sample-buildout/bin/sphinx-build'.
    <BLANKLINE>
