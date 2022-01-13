class IncorrectListFilling(Exception):
    def __init__(self):
        super().__init__("Неверное заполнение списка программ")


class NoListFile(Exception):
    def __init__(self):
        super().__init__("Файл: 'Programs.txt' не найден, переустановите программу или создайте его самостоятельно")


class IconExtractionError(Exception):
    def __init__(self, path):
        super().__init__(f"Невозможно извлечь иконку из файла по пути: '{path}'")


class StartError(Exception):
    def __init__(self, path):
        super().__init__(f"Невозможно запустить программу по пути:'{path}'")


class IncorrectPath(Exception):
    def __init__(self, path):
        super().__init__(f"Путь: '{path}' не указывает на программу")
