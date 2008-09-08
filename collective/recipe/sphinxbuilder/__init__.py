# -*- coding: utf-8 -*-
"""Recipe sphinxbuilder"""
from os.path import join, exists
from datetime import datetime
import os
import sys

from sphinx.quickstart import QUICKSTART_CONF
from sphinx.quickstart import MAKEFILE
from sphinx.quickstart import MASTER_FILE
from sphinx.util import make_filename

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
        bin = self.buildout['buildout']['bin-directory']
        script_name = self.options.get('script-name', self.name) 
        doc_directory = self.options.get('doc-directory', 
                                         join(root, 'docs'))

        if sys.platform == 'win32':
            DOT = '_'
        else:
            DOT = '.'

        self.options['now'] = datetime.now().ctime() 
        year = datetime.now().year      
        suffix = '.txt'
        for name, val in (('project', 'Plone'),  
                          ('extensions', ''), 
                          ('master', 'index'),
                          ('year', str(year)),
                          ('suffix', suffix), 
                          ('author', 'Plone Community'),
                          ('version', '1.0'), 
                          ('release', '1.0'),
                          ('dot', DOT),
                          ('sep', 'yes')):
            bname = 'sphinx-%s' 
            self.options[name] = self.options.get(bname, val)          

        self.options['project_fn'] = make_filename(self.options['project'])
        separate = self.options['sep'].upper() in ('Y', 'YES')
        self.options['rsrcdir'] = separate and 'source' or '.'
        self.options['rbuilddir'] = separate and 'build' or DOT + 'build'
 
        lines = [l for l in 
                 self.options.get('doc-outputs', 'html').split('\n')
                 if l.strip() != '']

        doc_outputs = [e.strip() for e in lines]

        if not exists(doc_directory):
            os.mkdir(doc_directory)
            
            # let's create the initial structure
            conf = QUICKSTART_CONF % self.options
            make = MAKEFILE % self.options
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
            
            os.mkdir(join(source_dir, '%stemplates' % DOT))
            os.mkdir(join(source_dir, '%sstatic' % DOT))  

            # we will add goodies here later

        # now lets create the script used to generate docs
        latex_directory = os.path.join(doc_directory, 'build',
                                       'latex')
        script = ['cd %s' % doc_directory]
        if 'html' in doc_outputs:
            script.append('make html')
        if 'latex' in doc_outputs:
            script.append('make latex')
        if 'pdf' in doc_outputs:
            script.append('make latex && cd %s && make' % latex_directory)

        make_doc = join('bin', script_name)
        self._write_file(make_doc, '\n'.join(script)) 
        os.chmod(make_doc, 0777) 
        return (make_doc,)

    update = install

