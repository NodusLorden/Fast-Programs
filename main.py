from pymsgbox import alert
from infi.systray import SysTrayIcon

from Components.linkbuttons import Buttons
from Components.MyExceptions import IncorrectPath, StartError, NoListFile, IncorrectListFilling


def get_programs() -> list:
    try:
        with open("Programs.txt", mode="r", encoding="UTF-8") as f:
            programs = list(filter(lambda st: st, f.read().split("\n")))  # filter void str

    except FileNotFoundError:
        raise NoListFile

    except Exception:
        raise IncorrectListFilling

    return programs


def main():

    menu_options = []

    try:
        programs = get_programs()

    except Exception as er:
        alert(er, "TrayLink: Ошибка")
        return

    for path in programs:
        try:
            pr = Buttons(path)
            menu_options.append(pr.get_option())

        except IncorrectPath as er:
            alert(er, "TrayLink: Ошибка")
            continue

    menu_options.append(("Clean cache", None, Buttons.clean_cache))

    with SysTrayIcon("Components/icon.ico", "TrayLink", tuple(menu_options)) as systray:
        systray.update()


if __name__ == '__main__':
    main()
