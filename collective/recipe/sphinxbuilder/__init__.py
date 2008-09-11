# -*- coding: utf-8 -*-
"""Recipe sphinxbuilder"""
from os.path import join, exists
from datetime import datetime
import os
import sys
import shutil
import re

import zc.buildout
import zc.recipe.egg

from sphinx.quickstart import QUICKSTART_CONF
from sphinx.quickstart import MAKEFILE
from sphinx.quickstart import MASTER_FILE
from sphinx.util import make_filename

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)

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
        self.options['rbuilddir'] = (separate and 'build' or 
                                     self.options['sphinx-dot'] + 
                                     'build')
        self.options['underline'] = '=' * len(self.options['project'])
        lines = [l for l in 
                 self.options.get('doc-outputs', 'html').split('\n')
                 if l.strip() != '']

        doc_outputs = [e.strip() for e in lines]

        if not exists(doc_directory):
            os.mkdir(doc_directory)
            
            current_dir = os.path.dirname(__file__)
            static_dir = join(current_dir, 'static')
            templates = join(current_dir, 'templates') 
            source_dir = join(doc_directory, 'source')
            dot = self.options['dot']
            target_templates = join(source_dir, '%stemplates' % dot)
            target_static = join(source_dir, '%sstatic' % dot)
            
            os.mkdir(source_dir)
            os.mkdir(target_templates)
            os.mkdir(target_static)

            logo = self.options.get('sphinx-logo',
                                    join(static_dir, 'plone_logo.png'))
            # logo 
            target_logo = join(target_static, os.path.split(logo)[-1])
            shutil.copyfile(logo, target_logo)

            tex = self.options.get('sphinx-latex-options', 
                                   join(templates, 'options.tex')) 
            # latex options
            target_tex = join(target_static, os.path.split(tex)[-1])
            shutil.copyfile(tex, target_tex)
            tex_content = "open('%s').read()" % target_tex
            
            # let's create the initial structure
            conf = QUICKSTART_CONF % self.options

            # crappy, should provide our own template
            # but if sphinx one is changed...
            for source, target in (('#html_logo = None', 
                                    "html_logo ='%s'" % target_logo),
                                   ('#latex_logo = None', 
                                    "latex_logo='%s'" % target_logo),
                                   ("#latex_preamble = ''",
                                    "latex_preamble = %s" % tex_content)):

                conf = conf.replace(source, target)
            
            make = MAKEFILE % self.options
            sphinx_build = join(bin, 'sphinx-build')
            c = re.compile(r'^SPHINXBUILD .*$', re.M)

            make = c.sub(r'SPHINXBUILD = %s' % sphinx_build, make)
            master = MASTER_FILE % self.options

            # Makefile
            make_file = join(doc_directory, 'Makefile')
            self._write_file(make_file, make)
            
            # source dir with conf.py
            conf_file = join(source_dir, 'conf.py') 
            self._write_file(conf_file, conf)

            # index.txt
            index_file = join(source_dir, 'index%s' % self.options['suffix'])
            self._write_file(index_file, master)
            
            
            # and the static files

            # css
            css  = self.options.get('sphinx-css', 
                                    join(static_dir, 'plone.css'))
            target_css =  join(target_static, os.path.split(css)[-1])
            shutil.copyfile(css, target_css)
           
                        
            for f in ('search.html', 'layout.html', 'modindex.html'):
                
                content = open(join(templates, f)).read() 
                content = content % {'css': target_css}
                self._write_file(join(target_templates, f), content)
            
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

        # ad make sure we have sphinx-build
        requirements, ws = self.egg.working_set(['Sphinx'])

        zc.buildout.easy_install.scripts(
                [('sphinx-build', 'sphinx', 'main')],
                ws, sys.executable, bin)

        return (make_doc,)

    update = install

