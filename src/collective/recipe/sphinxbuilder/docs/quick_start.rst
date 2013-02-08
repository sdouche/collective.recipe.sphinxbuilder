===========
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
    recipe = collective.recipe.sphinxbuilder
    source = ${buildout:directory}/docs-source
    build = ${buildout:directory}/docs
    


Run your buildout and you will get a few new scripts in the `bin` folder,
called:

    - `sphinx-quickstart`, to quickstart sphinx documentation
    - `sphinxbuilder`, script that will 

To quickstart a documentation project run, as you would normaly do with Sphinx::

    $ bin/sphinx-quickstart

and anwser few questions and choose `docs-source` as you source folder.

To build your documentation, just run the sphinx script::

    $ bin/sphinxbuilder

That's it!

You will get a shiny Sphinx documenation in `docs/html`.
Write your documentation, go in `docs-source`.
Everytime source is modified, `sphinxbuilder` run script again.

A good starting point to write your documentation is: 
http://sphinx.pocoo.org/contents.html.


=======
Plone 4
=======

Usage with Plone 4 is even easier::

    [buildout]
    parts =
        ...
        sphinxbuilder
        ...
    
    [sphinxbuilder]
    recipe = collective.recipe.sphinxbuilder
    interpreter = ${buildout:directory}/bin/zopepy

Follow quick-start tutorial and do not forget to add interpreter with
installed eggs to access your sourcecode with Sphinx.
