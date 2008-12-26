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

        self.build_directory = options.get('build_directory', os.path.join(self.buildout_directory, 'docs'))
        self.source_directory = options.get('source', os.path.join(self.build_directory, 'source'))
        self.latex_directory = os.path.join(self.build_directory, 'latex')

    def install(self):
        """Installer"""

        # CREATE NEEDED DIRECTORIES
        layout_options = {}
        if not os.path.exists(self.build_directory):
            os.mkdir(self.build_directory)
        if not os.path.isabs(self.source_directory):
            self.source_directory = self._resolve_path(self.source_directory)
        else:
            if not os.path.exists(self.source_directory):
                os.mkdir(self.source_directory)
            # LAYOUT (apply starting layout only if we are in "develop" mode)
            if 'layout' in self.options:
                self.layout_directory = self._resolve_path(self.options['layout'])
                for item in ['static', 'templates']:
                    src_path = os.path.join(self.layout_directory, item)
                    dst_path = os.path.join(self.source_directory, self.dot+item)
                    if os.path.exists(src_path) and not os.path.exists(dst_path):
                        shutil.copytree(src_path, dst_path)
                eval(compile(open(os.path.join(self.layout_directory, 'conf.py')).read(),
                        '', 'exec'), globals(), layout_options)
            for item in ['static', 'templates']:
                path = os.path.join(self.source_directory, self.dot+item)
                if not os.path.exists(path): os.mkdir(path)

        # default sphinxbuilder options
        for name, value in [
                ('project', self.name), ('extensions', ''), ('exclude_trees', ''),
                ('author', ''), ('copyright', ''), ('version', '1.0'), ('release', '1.0'),
                ('master', 'index'), ('suffix', '.txt'), ('now', str(datetime.now().ctime())),
                ('dot', sys.platform=='win32' and '_' or '.'), ('project_doc_texescaped', ''),
                ('year', str(datetime.now().year)), ('author_texescaped', ''),
                ('logo', ''), ('latex_options', '')]:
            if name not in self.options:
                if name in layout_options:
                    self.options[name] = layout_options[name]
                else:
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

    def resolveEntryPoint(self, source):
        distributions, ws = self.egg.working_set()
        
        # ENTRY POINTS 
        if ENTRY_POINT not in distributions:
            distributions.append(ENTRY_POINT)
        conf_options, entry_points = {}, []
        for dist in reversed(distributions):
    
            # FIND ENTRY POINT
            entry_point = ws.require(dist)[0].get_entry_map(ENTRY_POINT)
            if 'default' not in entry_point.keys():
                continue
            entry_point = entry_point['default'].load()
            entry_point_path = os.path.dirname(entry_point.__file__)
            entry_points.append(entry_point_path)

            # IMPORT conf.py OPTIONS FROM ENTRY POINT
            dist_conf = self._import_conf(entry_point.__name__)
            if dist_conf:
                for option in ['project', 'extensions', 'exclude_trees',
                               'author', 'copyright', 'version', 'release',
                               'master', 'suffix', 'dot', 'now', 'year',
                           'logo', 'latex_options', 'project_doc_texescaped',
                           'author_texescaped']:
                    conf_options[option] = getattr(dist_conf, option,
                                           conf_options.get(option, ''))
                    # TODO: extensions is list like option 
                    # we should append from parent entry points

    def _write_file(self, name, content):
        f = open(name, 'w')
        try:
            f.write(content)
        finally:
            f.close()

