# -*- coding: utf-8 -*-
"""Recipe sphinxbuilder"""

import os
import re
import sys
import shutil
import zc.buildout
import zc.recipe.egg
from datetime import datetime

from sphinx.quickstart import QUICKSTART_CONF
from sphinx.quickstart import MAKEFILE
from sphinx.quickstart import MASTER_FILE
from sphinx.util import make_filename


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        self.buildout_directory = self.buildout['buildout']['directory']
        self.bin_directory = self.buildout['buildout']['bin-directory']
        self.parts_directory = self.buildout['buildout']['parts-directory']

        self.script_name = options.get('script-name', name)
        self.product_directories = options.get('product_directories', '')
        self.outputs = [o.strip() for o in options.get('outputs', 'html').split() if o.strip()!='']
        self.dot = sys.platform=='win32' and '_' or '.'

        self.build_directory = options.get('build_directory',
                                    os.path.join(self.buildout_directory, 'docs'))
        self.source_directory = options.get('source', os.path.join(self.build_directory, 'source'))
        self.latex_directory = os.path.join(self.build_directory, 'latex')

    def install(self):
        """Installer"""

        # MAKEFILE
        c = re.compile(r'^SPHINXBUILD .*$', re.M)
        make = c.sub(r'SPHINXBUILD = %s' % (
               os.path.join(self.bin_directory, 'sphinx-build')),
               MAKEFILE % self.options)
        self._write_file(os.path.join(self.build_directory, 'Makefile'), make)


        # IF THERE IS NO MASTER FILE WE PROVIDE SPHINX DEFAULT ONE
        if not os.path.exists(os.path.join(
                self.source_directory, 'index%s' % self.options['suffix'])):
            self._write_file(os.path.join(
                    self.source_directory, 'index%s' % self.options['suffix']),
                    MASTER_FILE % self.options)

        # SPHINXBUILDER SCRIPT
        script = ['cd %s' % self.build_directory]
        if 'html' in self.outputs:
            script.append('make html')
        if 'latex' in self.outputs:
            script.append('make latex')
        if 'pdf' in self.outputs:
            script.append('make latex && cd %s && make' % self.latex_directory)
        sphinxbuilder_script = os.path.join(self.bin_directory, self.script_name)
        self._write_file(sphinxbuilder_script, '\n'.join(script))
        os.chmod(sphinxbuilder_script, 0777)

        # Setup extra Products namespace for old-style Zope products.
        initialization = ''
        product_directories = [d.strip() for d in self.product_directories.split()]
        if product_directories:
            initialization = 'import Products;'
            for product_directory in product_directories:
                initialization += ('Products.__path__.append(r"%s");' %
                                   product_directory)

        # SPHINX-BUILD
        requirements, ws = self.egg.working_set(['Sphinx', 'docutils'])
        extra_paths = self.options.get('extra_paths', None)
        if extra_paths:
            zc.buildout.easy_install.scripts(
                    [('sphinx-build', 'sphinx', 'main')], ws,
                    self.buildout[self.buildout['buildout']['python']]['executable'],
                    self.bin_directory,
                    extra_paths = extra_paths.split(),
                    initialization = initialization)
        else:
            zc.buildout.easy_install.scripts(
                    [('sphinx-build', 'sphinx', 'main')], ws,
                    self.buildout[self.buildout['buildout']['python']]['executable'],
                    self.bin_directory,
                    initialization = initialization)

        return [sphinxbuilder_script,]
    
    update = install

    def _resolve_path(self, source):
        source = source.split(':')
        dist, ws = self.egg.working_set([source[0]])
        source_directory = ws.by_key[source[0]].location

        # check for namespace name (eg: my.package will resolve as my/package)
        namespace_packages = source[0].split('.')
        if len(namespace_packages)>=1:
            source_directory = os.path.join(source_directory, *namespace_packages)

        if len(source)==2:
            source_directory = os.path.join(source_directory, source[1])
        return source_directory

    def _get_option(self, name):
        if name in self.options:
            return self.options[name]

    def _write_file(self, name, content):
        f = open(name, 'w')
        try:
            f.write(content)
        finally:
            f.close()

class WriteRecipe(Recipe):

    def install(self):
        # CREATE NEEDED DIRECTORIES
        if not os.path.exists(self.build_directory):
            os.mkdir(self.build_directory)
        if not os.path.isabs(self.source_directory):
            self.source_directory = self._resolve_path(self.source_directory)
        if not os.path.exists(self.source_directory):
            os.mkdir(self.source_directory)
            os.mkdir(os.path.join(self.source_directory, self.dot+'static'))

        # default sphinxbuilder options
        for name, default_value in [
                    ('project', self.name),
                    ('extensions', ''),
                    ('exclude_trees', ''),
                    ('author', ''),
                    ('copyright', ''),
                    ('version', '1.0'),
                    ('release', '1.0'),
                    ('master', 'index'),
                    ('suffix', '.txt'),
                    ('now', str(datetime.now().ctime())),
                    ('dot', sys.platform=='win32' and '_' or '.'),
                    ('project_doc_texescaped', ''),
                    ('year', str(datetime.now().year)),
                    ('author_texescaped', ''),
                    ('logo', ''),
                    ('latex_options', '')]:
            value = self._get_option(name)
            if not value: value = default_value
            if name == 'extensions': value = str(value.split())[1:-1]
            self.options[name] = value

        self.options['project_fn'] = make_filename(self.options['project'])
        self.options['project_doc'] = self.options['project']
        self.options['underline'] = '='*len(self.options['project'])
        self.options['rsrcdir'] = self.source_directory
        self.options['rbuilddir'] = self.build_directory

        # CREATE conf.py FILE
        # crappy, should provide our own template
        # but if sphinx one is changed...
        source_conf = os.path.join(self.source_directory, 'conf.py')
        if not os.path.exists(source_conf):
            conf = QUICKSTART_CONF % self.options
            if self.options.get('logo', None):
                logo = os.path.join(self.source_directory,
                            '%sstatic' % self.options['dot'], self.options['logo'])
                conf = conf.replace('#html_logo = None', "html_logo='%s'" % logo)
                conf = conf.replace('#latex_logo = None', "latex_logo='%s'" % logo)
            if self.options.get('latex_options', None):
                tex = "open('%s').read()" % os.path.join(
                                    self.source_directory, '%sstatic' %
                                    self.options['dot'], self.options['latex_options'])
                conf = conf.replace("#latex_preamble = ''", "latex_preamble = %s" % tex)
            self._write_file(os.path.join(self.source_directory, 'conf.py'), conf)

        return Recipe.install(self)


class LayoutRecipe(WriteRecipe):
    layout_templates = None
    layout_static = None
    
    def install(self):
        if not os.path.exists(self.build_directory):
            os.mkdir(self.build_directory)
        if not os.path.isabs(self.source_directory):
            self.source_directory = self._resolve_path(self.source_directory)
        if not os.path.exists(self.source_directory):
            os.mkdir(self.source_directory)
        
        dst_templates = os.path.join(self.source_directory, self.dot+'templates')
        if self.layout_templates and \
                os.path.exists(self.layout_templates) and \
                not os.path.exists(dst_templates):
            shutil.copytree(self.layout_templates, dst_templates)

        dst_static = os.path.join(self.source_directory, self.dot+'static')
        if self.layout_static and \
                os.path.exists(self.layout_static) and \
                not os.path.exists(dst_static):
            shutil.copytree(self.layout_static, dst_static)

        return WriteRecipe.install(self)


class PloneRecipe(LayoutRecipe):
    
    layout_templates = os.path.join(os.path.dirname(__file__), 'plone', 'templates')
    layout_static = os.path.join(os.path.dirname(__file__), 'plone', 'static')

    def _get_option(self, name):
        default_options = dict(
            project         = 'Plone',
            author          = 'Plone Community',
            copyright       = str(datetime.now().year)+', Plone Community',
            logo            = 'logo.png',
            latex_options   = 'options.tex')
        if name in default_options and name not in self.options:
            return default_options[name]



