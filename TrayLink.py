import os
from PIL import Image

from infi.systray import SysTrayIcon
import extract_icon
import win32com.client

from MyExceptions import *


def get_programs() -> list:
    try:
        with open("Programs.txt", mode="r", encoding="UTF-8") as f:
            programs = list(filter(lambda st: st, f.read().split("\n")))  # filter void str

    except FileNotFoundError:
        raise NoListFile

    except Exception:
        raise IncorrectListFilling

    return programs


def clean_cache():
    d = "IconCache/"
    for icon in os.listdir(d):
        if icon.endswith(".ico"):
            os.remove(os.path.join(d, icon))


class PrButtons:

    def __init__(self, path: str):
        self._path = self._getrealpath(path)
        self._name = self._getfilename(self._path)
        self._iconpath = "IconCache\\" + self._name + ".ico"

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
    def _getrealpath(cls, path):
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
    def _getfilename(cls, path):
        return os.path.split(path)[-1].rstrip(".exe")


def main():

    menu_options = []

    for path in get_programs():

        try:
            pr = PrButtons(path)
            menu_options.append(pr.get_option())
        except IncorrectPath:
            continue

    menu_options.append(("Clean cache", None, clean_cache))

    systray = SysTrayIcon("icon.ico", "Programs", tuple(menu_options))

    try:
        systray.start()
    except StartError:
        pass


if __name__ == '__main__':
    main()
