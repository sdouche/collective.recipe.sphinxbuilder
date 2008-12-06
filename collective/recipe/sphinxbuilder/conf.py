
import sys
from datetime import datetime

project         = 'Plone'
extensions      = ''
exclude_trees   = ''
author          = 'Plone Community'
copyright       = str(datetime.now().year)+', Plone Community'
version         = '1.0'
release         = '1.0'
master          = 'index'
suffix          = '.txt'
dot             = sys.platform=='win32' and '_' or '.'
now             = datetime.now().ctime()
year            = str(datetime.now().year)
logo            = 'logo.png'
latex_options   = 'options.tex'
project_doc_texescaped = ''
author_texescaped = ''
