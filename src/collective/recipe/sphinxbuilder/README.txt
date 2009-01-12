What is Sphinx ?
================

Sphinx is the rising tool in the Python community to build
documentation. See http://sphinx.pocoo.org.

It is now used for instance by Python. See http://docs.python.org/dev and many
others 

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
        sphinxbuilder
        ...
    
    [sphinxbuilder]
    recipe = collective.recipe.sphinxbuilder:write


That's it ! Run your buildout and you will get:

- a new script in the `bin` folder, called  `sphinxbuilder`
- a `parts/sphinxbuilder` directory containing your documentation.

To build your documentation, just run the sphinx script::

    $ bin/sphinxbuilder

You will get a shiny Sphinx documenation in `docs/html`.
To write your documentation, go in `docs/source`, if there is none create it.
Everytime source is modified, run the buildout and script again.

A good starting point to write your documentation is: 
http://sphinx.pocoo.org/contents.html.

Supported options
=================

The recipe supports the following options:

docs-directory
    Specify the build documentation root. Default to `docs`.    

outputs
    Multiple-line value that defines what kind of output to produce. 
    Can be `html`, `latex` or `pdf`. Defaults to `html`.

script-name
    The name of the script generated. Defaults to the name of the section.    

project
    The name of the project used in Plone. Defaults to Plone.

extensions
    Sphinx extensions in use. Defaults to none. 

master 
    Name of the index file. Defaults to `index`.

year
    Year of the project. Defaults to current year.

suffix
    File extensions used for reST file. Defaults to .txt

author
    Author. Defaults to Plone Community. 

version
    Version. Defaults to 1.0.

release
    Release. Defaults to 1.0.

dot 
    The prefix of the static and template directory.
    Defaults to '.' under Linux and '_' under Windows.

logo 
    Logo used for html and pdf. Defaults to plone.png 
    (which is provided by the recipe)

css
    css file used to change Sphinx look. Defaults to 
    plone.css (which is provided by the recipe)

latex_options
    extra latex options file used in Sphinx. Defaults to options.tex
    provided by the recipe. 

extra_paths
    Extra paths to be inserted into sys.path.

product_directories
    Extra product directories to be extend the Products namespace for
    old-style Zope Products.

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
    ... recipe = collective.recipe.sphinxbuilder:write
    ... project = SphinxBuilder
    ... version = 0.5.1
    ... release = 0.5.1
    ... """) 

Let's run the buildout::

    >>> print 'start', system(buildout) 
    start...
    Installing sphinxbuilder.
    collective.recipe.sphinxbuilder: creating conf.py file..
    collective.recipe.sphinxbuilder: writing MAKEFILE..
    collective.recipe.sphinxbuilder: writing master file..
    collective.recipe.sphinxbuilder: writing sphinxbuilder script..
    Generated script '/sample-buildout/bin/sphinx-build'.
    <BLANKLINE>

What are we expecting ? 

A `docs` folder with a Sphinx structure::

    >>> docs = join(sample_buildout, 'docs')
    >>> ls(docs)
    - Makefile
    d  source

    >>> source = join(sample_buildout, 'docs', 'source')
    >>> ls(source) 
    d  .static
    -  conf.py
    -  index.txt

A script in the `bin` folder to build the docs::

    >>> bin = join(sample_buildout, 'bin')
    >>> ls(bin)
    - buildout
    - sphinx-build
    - sphinxbuilder

The content of the script is a simple shell script::

    >>> script = join(sample_buildout, 'bin', 'sphinxbuilder')
    >>> print open(script).read()
    cd ...docs
    make html
    
    >>> print 'start', system(script)
    start mkdir -p /sample-buildout/docs/html /sample-buildout/docs/doctrees
    ...
   
If we want `latex` and `pdf`, we need to explicitly define it::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = sphinxbuilder
    ...
    ... [sphinxbuilder]
    ... recipe = collective.recipe.sphinxbuilder
    ... outputs = html latex pdf
    ... """) 
    >>> print 'start', system(buildout)
    start Uninstalling sphinxbuilder.
    Installing sphinxbuilder.
    collective.recipe.sphinxbuilder: writing MAKEFILE..
    collective.recipe.sphinxbuilder: writing sphinxbuilder script..
    <BLANKLINE>

Let's see our script now::
    
    >>> cat(script)
    cd ...docs
    make html
    make latex
    make latex && cd ... && make

Finally let's run it::

    >>> print 'start', system(script)
    start mkdir -p /sample-buildout/docs/html /sample-buildout/docs/doctrees
    ...
    Transcript written in modSphinxBuilder.ilg.
    <BLANKLINE>

We should have some nice reST file::

    >>> print open(join(source, 'index.txt')).read()
    .. SphinxBuilder documentation master file, ...
    <BLANKLINE>
    Welcome to SphinxBuilder's documentation!
    =========================================
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

