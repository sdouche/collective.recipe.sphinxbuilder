What is Sphinx ?
================

Sphinx is the rising tool in the Python community to build
documentation. See http://sphinx.pocoo.org.

It is now used for instance by Python. See http://docs.python.org/dev.

Sphinx uses reStructuredText, and can be used to write your buildout-based
application. This recipe sets everything up for you, so you can
provide a nice-looking documentation within your buildout, in static html
or even PDF.

The fact that your documentation is managed like your code
makes it easy to maintain and change it.

Quick start
===========

To use the recipe, add in your buildout configuration file
a section like this::

    [buildout]
    parts =
        ...
        sphinx
        ...
    
    [sphinx]
    recipe = collective.recipe.sphinxbuilder

That's it ! Run your buildout and you will get:

- a new script in the `bin` folder, called  `sphinx`
- a `docs` directory containing your documentation.

To build your documentation, just run the sphinx script::

    $ bin/sphinx

You will get a shiny Sphinx documenation in `docs/build/html`.
To write your documentation, go in `docs/source`.
Everytime source is modified, run the script again.

A good starting point to write your documentation is: http://sphinx.pocoo.org/contents.html.
   
Supported options
=================

The recipe supports the following options:

doc-directory
    Specify the documentation root. Default to `docs`.    

doc-outputs
    Multiple-line value that defines what kind of output to produce. 
    Can be `html`, `latex` or `pdf`. Defaults to `html`.

script-name
    The name of the script generated. Defaults to the name of the section.    

sphinx-project
    The name of the project used in Plone. Defaults to Plone.

sphinx-extensions
    Sphinx extensions in use. Defaults to none. 

sphinx-master 
    Name of the index file. Defaults to index.

sphinx-year
    Year of the project. Defaults to current year.

sphinx-suffix
    File extensions used for reST file. Defaults to .txt

sphinx-author
    Author. Defaults to Plone Community. 

sphinx-version
    Version. Defaults to 1.0.

sphinx-release
    Release. Defaults to 1.0.

sphinx-dot 
    The prefix of the static and template directory.
    Defaults to '.' under Linux and '_' under Windows.

sphinx-sep
    Separate source and build directories. (Y or N) 
    Defaults to Yes.

sphinx-logo 
    Logo used for html and pdf. Defaults to plone.png 
    (which is provided by the recipe)

sphinx-css
    css file used to change Sphinx look. Defaults to 
    plone.css (which is provided by the recipe)

sphinx-latex-options
    extra latex options file used in Sphinx. Defaults to options.tex
    provided by the recipe. 

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
    Generated script '/sample-buildout/bin/sphinx-build'.
    <BLANKLINE>

What are we expecting ? 

A `docs` folder with a Sphinx structure::

    >>> docs = join(sample_buildout, 'docs')
    >>> ls(docs)
    - Makefile
    d source

    >>> source = join(docs, 'source')
    >>> ls(source) 
    d  .static
    d  .templates
    -  conf.py
    -  index.txt

    >>> ls(join(source, '.templates'))
    -  layout.html
    -  modindex.html
    -  search.html

    >>> ls(join(source, '.static'))
    -  options.tex
    -  plone.css
    -  plone_logo.png

A script in the `bin` folder to build the docs::

    >>> bin = join(sample_buildout, 'bin')
    >>> ls(bin)
    - buildout
    - sphinx
    - sphinx-build

The content of the script is a simple shell script::

    >>> script = join(sample_buildout, 'bin', 'sphinx')
    >>> print open(script).read()
    cd ...docs
    make html
   
If we want `latex` and `pdf`, we need to explicitly define it::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = sphinx
    ...
    ... [sphinx]
    ... recipe = collective.recipe.sphinxbuilder
    ... doc-outputs =
    ...     html
    ...     latex
    ...     pdf
    ... """) 
    >>> print 'start', system(buildout)
    start...
    Installing sphinx.
    <BLANKLINE>

Let's see our script now::
    
    >>> print open(script).read() 
    cd ...docs
    make html
    make latex
    make latex && cd ... && make

Finally let's run it::

    >>> print 'start', system(script)
    start mkdir -p build/html build/doctrees
    ...
    Transcript written in modPlone.ilg.
    <BLANKLINE>

We should have some nice reST file::

    >>> print open(join(docs, 'source', 'index.txt')).read()
    .. Plone documentation master file, ...
    <BLANKLINE>
    Welcome to Plone's documentation!
    =================================
    <BLANKLINE>
    Contents:
    <BLANKLINE>
    .. toctree::
       :maxdepth: 2
    <BLANKLINE>
    Indices and tables
    ==================
    <BLANKLINE>
    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`
    <BLANKLINE>
    <BLANKLINE>

And the html rendering should use the plone logo::

    >>> html = open(join(docs, 'build', 'html', 'index.html')).read()
    >>> 'plone_logo.png' in html
    True


