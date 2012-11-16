MAKEFILE = '''\
# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = %(rbuilddir)s

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) \
$(SPHINXOPTS) %(rsrcdir)s
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) %(rsrcdir)s

.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp \
epub latex latexpdf text man changes linkcheck doctest gettext

help:
\t@echo "Please use \\`make <target>' where <target> is one of"
\t@echo "  html       to make standalone HTML files"
\t@echo "  warnings-html to make standalone HTML files (warnings become errors)"
\t@echo "  dirhtml    to make HTML files named index.html in directories"
\t@echo "  singlehtml to make a single large HTML file"
\t@echo "  pickle     to make pickle files"
\t@echo "  json       to make JSON files"
\t@echo "  htmlhelp   to make HTML files and a HTML help project"
\t@echo "  qthelp     to make HTML files and a qthelp project"
\t@echo "  devhelp    to make HTML files and a Devhelp project"
\t@echo "  epub       to make an epub"
\t@echo "  latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
\t@echo "  latexpdf   to make LaTeX files and run them through pdflatex"
\t@echo "  text       to make text files"
\t@echo "  man        to make manual pages"
\t@echo "  texinfo    to make Texinfo files"
\t@echo "  info       to make Texinfo files and run them through makeinfo"
\t@echo "  gettext    to make PO message catalogs"
\t@echo "  changes    to make an overview of all changed/added/deprecated items"
\t@echo "  linkcheck  to check all external links for integrity"
\t@echo "  doctest    to run all doctests embedded in the documentation \
(if enabled)"

clean:
\t-rm -rf $(BUILDDIR)/*

html:
\t$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
\t@echo
\t@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

warnings-html:
\t$(SPHINXBUILD) -W -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
\t@echo
\t@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

dirhtml:
\t$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
\t@echo
\t@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

singlehtml:
\t$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
\t@echo
\t@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

pickle:
\t$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
\t@echo
\t@echo "Build finished; now you can process the pickle files."

json:
\t$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
\t@echo
\t@echo "Build finished; now you can process the JSON files."

htmlhelp:
\t$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
\t@echo
\t@echo "Build finished; now you can run HTML Help Workshop with the" \\
\t      ".hhp project file in $(BUILDDIR)/htmlhelp."

qthelp:
\t$(SPHINXBUILD) -b qthelp $(ALLSPHINXOPTS) $(BUILDDIR)/qthelp
\t@echo
\t@echo "Build finished; now you can run "qcollectiongenerator" with the" \\
\t      ".qhcp project file in $(BUILDDIR)/qthelp, like this:"
\t@echo "# qcollectiongenerator $(BUILDDIR)/qthelp/%(project_fn)s.qhcp"
\t@echo "To view the help file:"
\t@echo "# assistant -collectionFile $(BUILDDIR)/qthelp/%(project_fn)s.qhc"

devhelp:
\t$(SPHINXBUILD) -b devhelp $(ALLSPHINXOPTS) $(BUILDDIR)/devhelp
\t@echo
\t@echo "Build finished."
\t@echo "To view the help file:"
\t@echo "# mkdir -p $$HOME/.local/share/devhelp/%(project_fn)s"
\t@echo "# ln -s $(BUILDDIR)/devhelp\
 $$HOME/.local/share/devhelp/%(project_fn)s"
\t@echo "# devhelp"

epub:
\t$(SPHINXBUILD) -b epub $(ALLSPHINXOPTS) $(BUILDDIR)/epub
\t@echo
\t@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

latex:
\t$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
\t@echo
\t@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
\t@echo "Run \\`make' in that directory to run these through (pdf)latex" \\
\t      "(use \\`make latexpdf' here to do that automatically)."

latexpdf:
\t$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
\t@echo "Running LaTeX files through pdflatex..."
\t$(MAKE) -C $(BUILDDIR)/latex all-pdf
\t@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

text:
\t$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
\t@echo
\t@echo "Build finished. The text files are in $(BUILDDIR)/text."

man:
\t$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man
\t@echo
\t@echo "Build finished. The manual pages are in $(BUILDDIR)/man."

texinfo:
\t$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
\t@echo
\t@echo "Build finished. The Texinfo files are in $(BUILDDIR)/texinfo."
\t@echo "Run \\`make' in that directory to run these through makeinfo" \\
\t      "(use \\`make info' here to do that automatically)."

info:
\t$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
\t@echo "Running Texinfo files through makeinfo..."
\tmake -C $(BUILDDIR)/texinfo info
\t@echo "makeinfo finished; the Info files are in $(BUILDDIR)/texinfo."

gettext:
\t$(SPHINXBUILD) -b gettext $(I18NSPHINXOPTS) $(BUILDDIR)/locale
\t@echo
\t@echo "Build finished. The message catalogs are in $(BUILDDIR)/locale."

changes:
\t$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
\t@echo
\t@echo "The overview file is in $(BUILDDIR)/changes."

linkcheck:
\t$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
\t@echo
\t@echo "Link check complete; look for any errors in the above output " \\
\t      "or in $(BUILDDIR)/linkcheck/output.txt."

doctest:
\t$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
\t@echo "Testing of doctests in the sources finished, look at the " \\
\t      "results in $(BUILDDIR)/doctest/output.txt."
'''

BATCHFILE = '''\
@ECHO OFF

REM Command file for Sphinx documentation

if "%%SPHINXBUILD%%" == "" (
\tset SPHINXBUILD=sphinx-build
)
set BUILDDIR=%(rbuilddir)s
set ALLSPHINXOPTS=-d %%BUILDDIR%%/doctrees %%SPHINXOPTS%% %(rsrcdir)s
set I18NSPHINXOPTS=%%SPHINXOPTS%% %(rsrcdir)s
if NOT "%%PAPER%%" == "" (
\tset ALLSPHINXOPTS=-D latex_paper_size=%%PAPER%% %%ALLSPHINXOPTS%%
\tset I18NSPHINXOPTS=-D latex_paper_size=%%PAPER%% %%I18NSPHINXOPTS%%
)

if "%%1" == "" goto help

if "%%1" == "help" (
\t:help
\techo.Please use `make ^<target^>` where ^<target^> is one of
\techo.  html       to make standalone HTML files
\techo.  warnings-html to make standalone HTML files (turn warnings into errors)
\techo.  dirhtml    to make HTML files named index.html in directories
\techo.  singlehtml to make a single large HTML file
\techo.  pickle     to make pickle files
\techo.  json       to make JSON files
\techo.  htmlhelp   to make HTML files and a HTML help project
\techo.  qthelp     to make HTML files and a qthelp project
\techo.  devhelp    to make HTML files and a Devhelp project
\techo.  epub       to make an epub
\techo.  latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter
\techo.  text       to make text files
\techo.  man        to make manual pages
\techo.  texinfo    to make Texinfo files
\techo.  gettext    to make PO message catalogs
\techo.  changes    to make an overview over all changed/added/deprecated items
\techo.  linkcheck  to check all external links for integrity
\techo.  doctest    to run all doctests embedded in the documentation if enabled
\tgoto end
)

if "%%1" == "clean" (
\tfor /d %%%%i in (%%BUILDDIR%%\*) do rmdir /q /s %%%%i
\tdel /q /s %%BUILDDIR%%\*
\tgoto end
)

if "%%1" == "html" (
\t%%SPHINXBUILD%% -b html %%ALLSPHINXOPTS%% %%BUILDDIR%%/html
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished. The HTML pages are in %%BUILDDIR%%/html.
\tgoto end
)

if "%%1" == "warnings-html" (
\t%%SPHINXBUILD%% -W -b html %%ALLSPHINXOPTS%% %%BUILDDIR%%/html
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished. The HTML pages are in %%BUILDDIR%%/html.
\tgoto end
)

if "%%1" == "dirhtml" (
\t%%SPHINXBUILD%% -b dirhtml %%ALLSPHINXOPTS%% %%BUILDDIR%%/dirhtml
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished. The HTML pages are in %%BUILDDIR%%/dirhtml.
\tgoto end
)

if "%%1" == "singlehtml" (
\t%%SPHINXBUILD%% -b singlehtml %%ALLSPHINXOPTS%% %%BUILDDIR%%/singlehtml
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished. The HTML pages are in %%BUILDDIR%%/singlehtml.
\tgoto end
)

if "%%1" == "pickle" (
\t%%SPHINXBUILD%% -b pickle %%ALLSPHINXOPTS%% %%BUILDDIR%%/pickle
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished; now you can process the pickle files.
\tgoto end
)

if "%%1" == "json" (
\t%%SPHINXBUILD%% -b json %%ALLSPHINXOPTS%% %%BUILDDIR%%/json
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished; now you can process the JSON files.
\tgoto end
)

if "%%1" == "htmlhelp" (
\t%%SPHINXBUILD%% -b htmlhelp %%ALLSPHINXOPTS%% %%BUILDDIR%%/htmlhelp
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished; now you can run HTML Help Workshop with the ^
.hhp project file in %%BUILDDIR%%/htmlhelp.
\tgoto end
)

if "%%1" == "qthelp" (
\t%%SPHINXBUILD%% -b qthelp %%ALLSPHINXOPTS%% %%BUILDDIR%%/qthelp
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished; now you can run "qcollectiongenerator" with the ^
.qhcp project file in %%BUILDDIR%%/qthelp, like this:
\techo.^> qcollectiongenerator %%BUILDDIR%%\\qthelp\\%(project_fn)s.qhcp
\techo.To view the help file:
\techo.^> assistant -collectionFile %%BUILDDIR%%\\qthelp\\%(project_fn)s.ghc
\tgoto end
)

if "%%1" == "devhelp" (
\t%%SPHINXBUILD%% -b devhelp %%ALLSPHINXOPTS%% %%BUILDDIR%%/devhelp
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished.
\tgoto end
)

if "%%1" == "epub" (
\t%%SPHINXBUILD%% -b epub %%ALLSPHINXOPTS%% %%BUILDDIR%%/epub
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished. The epub file is in %%BUILDDIR%%/epub.
\tgoto end
)

if "%%1" == "latex" (
\t%%SPHINXBUILD%% -b latex %%ALLSPHINXOPTS%% %%BUILDDIR%%/latex
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished; the LaTeX files are in %%BUILDDIR%%/latex.
\tgoto end
)

if "%%1" == "text" (
\t%%SPHINXBUILD%% -b text %%ALLSPHINXOPTS%% %%BUILDDIR%%/text
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished. The text files are in %%BUILDDIR%%/text.
\tgoto end
)

if "%%1" == "man" (
\t%%SPHINXBUILD%% -b man %%ALLSPHINXOPTS%% %%BUILDDIR%%/man
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished. The manual pages are in %%BUILDDIR%%/man.
\tgoto end
)

if "%%1" == "texinfo" (
\t%%SPHINXBUILD%% -b texinfo %%ALLSPHINXOPTS%% %%BUILDDIR%%/texinfo
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished. The Texinfo files are in %%BUILDDIR%%/texinfo.
\tgoto end
)

if "%%1" == "gettext" (
\t%%SPHINXBUILD%% -b gettext %%I18NSPHINXOPTS%% %%BUILDDIR%%/locale
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished. The message catalogs are in %%BUILDDIR%%/locale.
\tgoto end
)

if "%%1" == "changes" (
\t%%SPHINXBUILD%% -b changes %%ALLSPHINXOPTS%% %%BUILDDIR%%/changes
\tif errorlevel 1 exit /b 1
\techo.
\techo.The overview file is in %%BUILDDIR%%/changes.
\tgoto end
)

if "%%1" == "linkcheck" (
\t%%SPHINXBUILD%% -b linkcheck %%ALLSPHINXOPTS%% %%BUILDDIR%%/linkcheck
\tif errorlevel 1 exit /b 1
\techo.
\techo.Link check complete; look for any errors in the above output ^
or in %%BUILDDIR%%/linkcheck/output.txt.
\tgoto end
)

if "%%1" == "doctest" (
\t%%SPHINXBUILD%% -b doctest %%ALLSPHINXOPTS%% %%BUILDDIR%%/doctest
\tif errorlevel 1 exit /b 1
\techo.
\techo.Testing of doctests in the sources finished, look at the ^
results in %%BUILDDIR%%/doctest/output.txt.
\tgoto end
)

:end
'''
