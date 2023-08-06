from __future__ import unicode_literals
import os
import shutil

from .common import PostProcessor
from ..utils import (
    encodeFilename,
    make_dir,
    PostProcessingError,
)
from ..compat import compat_str


class MoveFilesAfterDownloadPP(PostProcessor):

    def __init__(self, downloader, files_to_move):
        PostProcessor.__init__(self, downloader)
        self.files_to_move = files_to_move

    @classmethod
    def pp_key(cls):
        return 'MoveFiles'

    def run(self, info):
        dl_path, dl_name = os.path.split(encodeFilename(info['filepath']))
        finaldir = info.get('__finaldir', dl_path)
        finalpath = os.path.join(finaldir, dl_name)
        self.files_to_move[info['filepath']] = finalpath

        for oldfile, newfile in self.files_to_move.items():
            if not newfile:
                newfile = os.path.join(finaldir, os.path.basename(encodeFilename(oldfile)))
            oldfile, newfile = compat_str(oldfile), compat_str(newfile)
            if os.path.abspath(encodeFilename(oldfile)) == os.path.abspath(encodeFilename(newfile)):
                continue
            if not os.path.exists(encodeFilename(oldfile)):
                self.report_warning('File "%s" cannot be found' % oldfile)
                continue
            if os.path.exists(encodeFilename(newfile)):
                if self.get_param('overwrites', True):
                    self.report_warning('Replacing existing file "%s"' % newfile)
                    os.path.remove(encodeFilename(newfile))
                else:
                    self.report_warning(
                        'Cannot move file "%s" out of temporary directory since "%s" already exists. '
                        % (oldfile, newfile))
                    continue
            make_dir(newfile, PostProcessingError)
            self.to_screen('Moving file "%s" to "%s"' % (oldfile, newfile))
            shutil.move(oldfile, newfile)  # os.rename cannot move between volumes

        info['filepath'] = compat_str(finalpath)
        return [], info
