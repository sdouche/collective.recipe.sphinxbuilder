# -*- coding: utf-8 -*-
"""Recipe sphinxbuilder"""
from os.path import join, exists
import os

from sphinx.quickstart import QUICKSTART_CONF
from sphinx.quickstart import MAKEFILE
from sphinx.quickstart import MASTER_FILE

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

    def _write_file(self, name, content):
        f = open(name, 'w')
        try:
            f.write(content)
        finally:
            f.close()

    def install(self):
        """Installer"""
        root = self.buildout['buildout']['directory']
        doc_directory = self.options.get('doc-directory', 
                                         join(root, 'docs'))
        
        if not exists(doc_directory):
            os.mkdir(doc_directory)
            
            # let's create the initial structure
            conf = QUICKSTART_CONF
            make = MAKEFILE
            master = MASTER_FILE

            # Makefile
            make_file = join(doc_directory, 'Makefile')
            self._write_file(make_file, make)
            
            # source dir with conf.py
            source_dir = join(doc_directory, 'source')
            os.mkdir(source_dir)
            conf_file = join(source_dir, 'conf.py') 
            self._write_file(conf_file, conf)

            # index.txt
            index_file = join(source_dir, 'index.txt')
            self._write_file(index_file, master)
            
            os.mkdir(join(source_dir, '_templates'))
            os.mkdir(join(source_dir, '_static'))  

            # we will add goodies here later

        # now lets create the scripts used to generate docs
        # XXX todo
        return tuple()

    update = install

