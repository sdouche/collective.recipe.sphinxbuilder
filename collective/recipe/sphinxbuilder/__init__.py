# -*- coding: utf-8 -*-
"""Recipe sphinxbuilder"""

import os
import re
import sys
import shutil
import zc.buildout
import zc.recipe.egg



from sphinx.quickstart import QUICKSTART_CONF
from sphinx.quickstart import MAKEFILE
from sphinx.quickstart import MASTER_FILE
from sphinx.util import make_filename

ENTRY_POINT = 'collective.recipe.sphinxbuilder'


class Recipe(object):
    """zc.buildout recipe"""
    

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)

        self.script_name = self.options.get('script-name', self.name)
        self.outputs = [output.strip() for output in 
                            self.options.get('outputs', 'html').split('\n')
                            if output.strip() != '']
        self.buildout_directory = self.buildout['buildout']['directory']
        self.bin_directory = self.buildout['buildout']['bin-directory']
        self.parts_directory = self.buildout['buildout']['parts-directory']
        self.source_directory = os.path.join(self.parts_directory, self.name)
        self.build_directory = self.options.get('docs-directory',
                               os.path.join(self.buildout_directory, 'docs'))
        self.latex_directory = os.path.join(self.build_directory, 'latex')
        self.product_directories = self.options.get('product_directories', '')

    def install(self):
        """Installer"""

        # CREATE NEEDED DIRECTORIES
        if not os.path.exists(self.source_directory):
            os.mkdir(self.source_directory)
        if not os.path.exists(self.build_directory):
            os.mkdir(self.build_directory)

        # EXTRA PATH IN working_set
        distributions, ws = self.egg.working_set([ENTRY_POINT])
        
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
                               'logo', 'latex_options']:
                    conf_options[option] = getattr(dist_conf, option,
                                           conf_options.get(option, ''))
                    # TODO: extensions is list like option 
                    # we should append from parent entry points


        # override options with buildout configuration
        for option, default in conf_options.items():
            self.options[option] = self.options.get(option, default)

        # IMPORT TEMPLATES, STATIC FILES
        for path in entry_points:
            self._import_templates(os.path.join(path, 'templates'))
            self._import_static(os.path.join(path, 'static'))
            self._import_source(os.path.join(path, 'source'))
       
        # OVERRIDE SOURCE FILES
        # TODO: should make it optional and provided through 'custom_source' option
        # TODO: this should be run with script_name script
        self._import_source(os.path.join(self.build_directory, 'source'))
        self._import_static(os.path.join(self.build_directory, 'source', 'static'))
        self._import_static(os.path.join(self.build_directory, 'source', 'templates'))

        # CREATE conf.py FILE
        self.options['project_fn'] = make_filename(self.options['project'])
        self.options['project_doc'] = self.options['project']
        self.options['underline'] = '='*len(self.options['project'])
        self.options['rsrcdir'] = self.source_directory
        self.options['rbuilddir'] = self.build_directory
        # crappy, should provide our own template
        # but if sphinx one is changed...
        logo = os.path.join(
                self.source_directory,
                '%sstatic' % self.options['dot'],
                self.options['logo'])
        tex = "open('%s').read()" % os.path.join(
                self.source_directory,
                '%sstatic' % self.options['dot'],
                self.options['latex_options'])
        conf = QUICKSTART_CONF % self.options
        for source, target in (('#html_logo = None', "html_logo ='%s'" % logo),
                               ('#latex_logo = None', "latex_logo='%s'" % logo),
                               ("#latex_preamble = ''", "latex_preamble = %s" % tex)):
            conf = conf.replace(source, target)
        self._write_file(os.path.join(self.source_directory, 'conf.py'), conf)

        # MAKEFILE
        c = re.compile(r'^SPHINXBUILD .*$', re.M)
        make = c.sub(r'SPHINXBUILD = %s' % (
               os.path.join(self.bin_directory, 'sphinx-build')),
               MAKEFILE % self.options)
        self._write_file(os.path.join(self.build_directory, 'Makefile'), make)


        # IF THERE IS NO MASTER FILE WE PROVIDE SPHINX DEFAULT ONE
        if not os.path.exists(os.path.join(self.source_directory,
                              'index%s' % self.options['suffix'])):
            self._write_file(os.path.join(self.source_directory,
                                          'index%s' % self.options['suffix']),
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
        requirements, ws = self.egg.working_set(['Sphinx'])
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

        return [self.source_directory, sphinxbuilder_script,]
    
    update = install

    def _import_conf(self, name):
        try:
            mod = __import__(name+'.conf')
            components = name.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp, None)
            return getattr(mod, 'conf', None)
        except:
            return None

    def _import_templates(self, path):
        self._import_folder('templates', path)

    def _import_static(self, path):
        self._import_folder('static', path)

    def _import_folder(self, folder, path):
        target = os.path.join(self.source_directory,
                              self.options['dot']+folder)
        if not os.path.exists(target):
            os.mkdir(target)
        for root, dirs, files in os.walk(path):
            for _file in files:
                shutil.copyfile(os.path.join(root, _file),
                                os.path.join(target, _file))

    def _import_source(self, path, target=None):
        if target == None:
            target = self.source_directory
        if not os.path.exists(target):
            os.mkdir(target)
        for root, dirs, files in os.walk(path):
            for _file in files:
                if _file.endswith(self.options['suffix']):
                    shutil.copyfile(os.path.join(root, _file),
                                    os.path.join(target, _file))
            for _dir in dirs:
                if _dir not in ['templates', 'static']:
                    self._import_source(os.path.join(root, _dir),
                                        os.path.join(target, _dir))

    def _write_file(self, name, content):
        f = open(name, 'w')
        try:
            f.write(content)
        finally:
            f.close()

