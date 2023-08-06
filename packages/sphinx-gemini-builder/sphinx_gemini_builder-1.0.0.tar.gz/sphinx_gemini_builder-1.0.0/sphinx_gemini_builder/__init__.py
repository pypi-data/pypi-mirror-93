#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Build Gemini blog from Sphinx.
"""

__version_info__ = (1, 0, 0)
__version__ = '.'.join([str(val) for val in __version_info__])


from os import path
from typing import Set, Dict, Any
from urllib.parse import quote

from sphinx.builders.text import TextBuilder
from sphinx.util import logging, status_iterator
from sphinx.util.osutil import copyfile, ensuredir,  relative_uri
from sphinx.locale import __
from sphinx.application import Sphinx
from sphinx.environment.adapters.asset import ImageAdapter
from docutils import nodes
from docutils.utils import relative_path

from .writer import GeminiTranslator, GeminiWriter

logger = logging.getLogger(__name__)


class GeminiBuilder(TextBuilder):
    """
    Gemini builder, based on native TextBuilder code from Sphinx
    """
    name = 'gemini'
    format = 'gemini'
    epilog = __('The gemini files are in %(outdir)s.')

    out_suffix = '.gmi'
    allow_parallel = True
    default_translator_class = GeminiTranslator

    current_docname = None

    def __init__(self, app) -> None:
        super().__init__(app)
        self.baseurl = self.config.gemini_baseurl
        self.images = []

    def prepare_writing(self, docnames: Set[str]) -> None:
        self.writer = GeminiWriter(self)

    def copy_image_files(self) -> None:
        """ From native HTML builder """
        if self.images:
            stringify_func = ImageAdapter(self.app.env).get_original_image_uri
            for src in status_iterator(
                self.images, __('copying images... '), "brown",
                len(self.images), self.app.verbosity,
                    stringify_func=stringify_func):
                destdir = path.dirname(src)
                destdir = path.join(self.outdir, self.imagedir, destdir)
                destdir = path.normpath(destdir)

                try:
                    ensuredir(destdir)
                    copyfile(path.join(self.srcdir, src),
                             path.join(self.outdir, self.imagedir, src))
                except Exception as err:
                    logger.warning(__('cannot copy image file %r: %s'),
                                   path.join(self.srcdir, src), err)

    def copy_download_files(self) -> None:
        """ From native HTML builder """
        def to_relpath(f: str) -> str:
            return relative_path(self.srcdir, f)

        # copy downloadable files
        if self.env.dlfiles:
            ensuredir(path.join(self.outdir, '_downloads'))
            for src in status_iterator(self.env.dlfiles, __('copying downloadable files... '),
                                       "brown", len(self.env.dlfiles), self.app.verbosity,
                                       stringify_func=to_relpath):
                try:
                    dest = path.join(self.outdir, '_downloads', self.env.dlfiles[src][1])
                    ensuredir(path.dirname(dest))
                    copyfile(path.join(self.srcdir, src), dest)
                except OSError as err:
                    logger.warning(__('cannot copy downloadable file %r: %s'),
                                   path.join(self.srcdir, src), err)

    def write_doc(self, docname: str, doctree: nodes.document) -> None:
        self.dlpath = relative_uri(self.get_target_uri(docname), '_downloads')
        self.imgpath = path.dirname(docname)
        super().write_doc(docname, doctree)

    def get_target_uri(self, docname: str, typ: str = None) -> str:
        return self.baseurl + quote(docname) + self.out_suffix

    def finish(self) -> None:
        self.finish_tasks.add_task(self.copy_image_files)
        self.finish_tasks.add_task(self.copy_download_files)
        super().finish()


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_builder(GeminiBuilder)
    app.add_config_value('gemini_footer', '', 'env')
    app.add_config_value('gemini_baseurl', '', 'env')

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
