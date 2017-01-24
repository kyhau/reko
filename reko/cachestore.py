"""
This script intends to assist avoiding recreating audio file by caching common audio files locally.
"""
from __future__ import print_function
import os
import string
from shutil import rmtree

DEDFAULT_LOCAL_CACHE_DIR = os.path.join(os.path.expanduser("~"), "reko.cache")
MAX_FILENAME_LEN = 250
TMP_IMAGE_NAME = "reko_img.png"


class CacheStore():
    def __init__(self):
        self._cache_dir = DEDFAULT_LOCAL_CACHE_DIR
        self._cache_img = None

    @property
    def cache_dir(self):
        if not os.path.exists(self._cache_dir):
            os.mkdir(self._cache_dir)
        return self._cache_dir

    @cache_dir.setter
    def cache_dir(self, value):
        self._cache_dir = value

    def get_filepath(self, filename):
        return os.path.join(self.cache_dir, filename)

    @property
    def cache_img(self):
        return self.get_filepath(TMP_IMAGE_NAME)

    def get_filename(self, txt, ext=None):
        """
        Determine a filename may help to identify the given message.
        :param txt: The message in text
        :param ext: file extension (e.g. mp4, png, etc)
        """
        new_filename = txt.lower().translate(None, string.punctuation).replace(' ','')
        new_filename = (new_filename[:MAX_FILENAME_LEN] + '..') \
            if len(new_filename) > MAX_FILENAME_LEN else new_filename
        if ext is not None:
            new_filename += '.{}'.format(ext)
        return new_filename

    def maintain_cache_dir(self, filename):
        if len(filename) > MAX_FILENAME_LEN:
            # Do not keep this file (filename may not contain entire message)
            f = os.path.join(self.cache_dir, filename)
            if os.path.exists(f):
                os.remove(f)

    def delete_cache_dir(self):
        if os.path.exists(self._cache_dir):
            rmtree(self._cache_dir)
