# -*- coding: utf-8 -*-
"""Recipe sphinxbuilder"""

import logging
import os
import re
import sys
import zc.buildout
import zc.recipe.egg
from fnmatch import fnmatch
from cStringIO import StringIO

log = logging.getLogger(__name__)


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        self.buildout_dir = self.buildout['buildout']['directory']
        self.bin_dir = self.buildout['buildout']['bin-directory']
        self.parts_dir = self.buildout['buildout']['parts-directory']

        self.interpreter = options.get('interpreter')
        self.product_dirs = options.get('products', '')
        self.outputs = options.get('outputs', 'html')

        self.build_dir = os.path.join(self.buildout_dir, options.get('build', 'docs'))
        self.source_dir = options.get('source', os.path.join(self.build_dir, 'source'))
        self.extra_paths = self.options.get('extra-paths', None)

        self.script_name = options.get('script-name', name)
        self.script_path = os.path.join(self.bin_dir, self.script_name)
        self.makefile_path = os.path.join(self.build_dir, 'Makefile')
        self.batchfile_path = os.path.join(self.build_dir, 'make.bat')

        self.re_sphinxbuild = re.compile(r'^SPHINXBUILD .*$', re.M)
        self.build_command = os.path.join(self.bin_dir, 'sphinx-build')
        if self.interpreter:
            self.build_command = ' '.join([self.interpreter, self.build_command])

    def install(self):
        """Installer"""

        # 1. CREATE BUILD FOLDER IF IT DOESNT EXISTS
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        # 2. RESOLVE SOURCE PATH
        if not os.path.isabs(self.source_dir):
            self.source_dir = self._resolve_path(self.source_dir)

        # we need extra_paths, e.g for docutils via fake-eggs
        # most probably this should be really fixed in buildout or the way
        # fake-zope-eggs messes with buildout - until then: This enables sphinx
        # to coexist in a buildout with fake-zope-eggs.
        extra_paths = []
        if self.extra_paths:
            for extra_path in self.extra_paths.split():
                dir = os.path.dirname(extra_path)
                for filename in os.listdir(dir):
                    filename = os.path.join(dir, filename)
                    if fnmatch(filename, extra_path):
                        extra_paths.append(filename)
            sys.path.extend(extra_paths)

        from utils import MAKEFILE
        from utils import BATCHFILE

        # and cleanup again
        if extra_paths:
            sys.path.reverse()
            for x in extra_paths:
                sys.path.remove(x)
            sys.path.reverse()

        # 3. CREATE MAKEFILE
        log.info('writing MAKEFILE..')
        self._write_file(self.makefile_path,
                         self.re_sphinxbuild.sub(r'SPHINXBUILD = %s' % (self.build_command),
                                                 MAKEFILE % dict(rsrcdir=self.source_dir,
                                                                 rbuilddir=self.build_dir,
                                                                 project_fn=self.script_name)))
        # 4. CREATE BATCHFILE
        log.info('writing BATCHFILE..')
        self._write_file(self.batchfile_path,
                         self.re_sphinxbuild.sub(r'SPHINXBUILD = %s' % (self.build_command),
                                                 BATCHFILE % dict(rsrcdir=self.source_dir,
                                                                  rbuilddir=self.build_dir,
                                                                  project_fn=self.script_name)))

        # 4. CREATE CUSTOM "sphinx-build" SCRIPT
        log.info('writing custom sphinx-builder script..')
        script = ['cd %s' % self.build_dir]
        if 'doctest' in self.outputs:
            script.append('make doctest')
        if 'html' in self.outputs:
            script.append('make html')
        if 'latex' in self.outputs:
            script.append('make latex')
        if 'epub' in self.outputs:
            script.append('make epub')
        if 'pdf' in self.outputs:
            latex = ''
            if 'latex' not in self.outputs:
                latex = 'make latex && '
            script.append(latex+'cd %s && make all-pdf' % os.path.join(self.build_dir, 'latex'))
        self._write_file(self.script_path, '\n'.join(script))
        os.chmod(self.script_path, 0777)

        # 5. INSTALL SPHINX WITH SCRIPT AND EXTRA PATHS

        # 5.1. Setup extra Products namespace for old-style Zope products.
        product_directories = [d for d in self.product_dirs.split()]
        if product_directories:
            initialization = 'import Products;'
            for product_directory in product_directories:
                initialization += ('Products.__path__.append(r"%s");' %
                                   product_directory)

        egg_options = {}
        if extra_paths:
            log.info('inserting extra-paths..')
            egg_options['extra_paths'] = extra_paths
        if product_directories:
            log.info('inserting products directories..')
            egg_options['initialization'] = initialization

        # WEIRD: this is needed for doctest to pass
        # :write gives error
        #       -> ValueError: ('Expected version spec in',
        #               'collective.recipe.sphinxbuilder:write', 'at', ':write')
        self.egg.name = self.options['recipe']
        requirements, ws = self.egg.working_set([self.options['recipe'], 'docutils'])
        zc.buildout.easy_install.scripts([('sphinx-quickstart', 'sphinx.quickstart', 'main'),
                                          ('sphinx-build', 'sphinx', 'main'),
                                          ('sphinx-apidoc', 'sphinx.apidoc', 'main'),
                                          ('sphinx-autogen', 'sphinx.ext.autosummary.generate', 'main')], ws,
                                         self.buildout[self.buildout['buildout']['python']]['executable'],
                                         self.bin_dir, **egg_options)

        # patch sphinx-build script
        # change last line from sphinx.main() to sys.exit(sphinx.main())
        # so that errors are correctly reported to Travis CI.
        sb = os.path.join(self.bin_dir, 'sphinx-build')
        temp_file = StringIO()
        sb_file = open(sb, 'r')
        for line in sb_file:
            temp_file.write(line.replace('sphinx.main()', 'sys.exit(sphinx.main())'))
        # open for writing (delete contents existing contents before rewriting
        # from StringIO that contains the modification
        sb_file = open(sb, 'w')
        sb_file.write(temp_file.getvalue())
        temp_file.close()
        sb_file.close()

        return [self.script_path, self.makefile_path, self.batchfile_path]

    update = install

    def _resolve_path(self, source):
        source = source.split(':')
        dist, ws = self.egg.working_set([source[0]])
        source_directory = ws.by_key[source[0]].location

        # check for namespace name (eg: my.package will resolve as my/package)
        # TODO
        namespace_packages = source[0].split('.')
        if len(namespace_packages) >= 1:
            source_directory = os.path.join(source_directory, *namespace_packages)

        if len(source) == 2:
            source_directory = os.path.join(source_directory, source[1])
        return source_directory

    def _write_file(self, name, content):
        f = open(name, 'w')
        try:
            f.write(content)
        finally:
            f.close()
