import os
from PIL import Image

import extract_icon
import win32com.client

from Components.MyExceptions import StartError, IncorrectPath


class Buttons:

    CACHE_DIR = "IconCache\\"

    def __init__(self, path: str):
        self._path = self._getrealpath(path)
        self._name = self._getfilename(self._path)

        self._iconpath = self.CACHE_DIR + self._name + ".ico"

        if not os.path.exists(self.CACHE_DIR):
            os.mkdir(self.CACHE_DIR)

        if not os.path.exists(self._iconpath):
            try:
                ex = extract_icon.ExtractIcon(self._path)

                icons = ex.get_group_icons()[0]

                im = ex.export(icons)
                im.save(self._iconpath, format='ICO')

            except Exception:
                Image.new("RGBA", (2, 2), color=(0, 0, 0, 0)).save(self._iconpath, format="ICO")  # void img for cache
                # raise IconExtractionError(self._path)

    def get_option(self):
        return self._name, self._iconpath, self.__call__

    def __call__(self, *args, **kwargs):
        try:
            os.startfile(self._path)
        except Exception:
            raise StartError(self._path)

    @classmethod
    def _getrealpath(cls, path: str):
        path = path.strip("'").strip('"')

        if not os.path.isfile(path):
            raise IncorrectPath(path)

        if path.endswith(".exe"):
            return path
        elif path.endswith(".lnk"):
            path = win32com.client.Dispatch("WScript.Shell").CreateShortCut(path).Targetpath
            return cls._getrealpath(path)
        else:
            raise IncorrectPath(path)

    @classmethod
    def _getfilename(cls, path: str):
        return os.path.split(path)[-1].rstrip(".exe")

    @classmethod
    def clean_cache(cls, _):
        for icon in os.listdir(cls.CACHE_DIR):
            if icon.endswith(".ico"):
                os.remove(os.path.join(cls.CACHE_DIR, icon))
