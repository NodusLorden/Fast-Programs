import pymsgbox

flog = (lambda *x: pymsgbox.alert(*x, "Ошибка"))


class MyExceptions(Exception):

    def __init__(self, *text):
        super().__init__(*text)
        flog(*text)


class IncorrectListFilling(MyExceptions):
    def __init__(self):
        super().__init__("Неверное заполнение списка программ")


class NoListFile(MyExceptions):
    def __init__(self):
        super().__init__("Файл: 'Programs.txt' не найден, переустановите программу или создайте его самостоятельно")


class IconExtractionError(MyExceptions):
    def __init__(self, path):
        super().__init__(f"Невозможно извлечь иконку из файла по пути: '{path}'")


class StartError(MyExceptions):
    def __init__(self, path):
        super().__init__(f"Невозможно запустить программу по пути:'{path}'")


class IncorrectPath(MyExceptions):
    def __init__(self, path):
        super().__init__(f"Путь: '{path}' не указывает на программу")
