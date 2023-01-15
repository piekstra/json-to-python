class PyLine:
    def __init__(self, line: str, indent_level: int):
        indent = '    ' * indent_level
        self.line: str = f'{indent}{line}\n'

    def __str__(self):
        return self.line


class PyClass:
    def __init__(self, name: str):
        self._lines: list[PyLine] = []
        self.import_decimal: bool = False
        self.class_name = ''.join([component.capitalize() for component in name.split('_')])

    def add_line(self, line: PyLine):
        self._lines.append(line)

    def get_lines(self):
        return self._lines


class PyClassList:
    def __init__(self):
        self.classes: list[PyClass] = []

    def add_class(self, pyclass: PyClass):
        self.classes.append(pyclass)

    def get_last_class(self):
        return self.classes[-1]

    def get_line_strings(self):
        all_lines = []
        if any(pyclass.import_decimal for pyclass in self.classes):
            all_lines.insert(0, PyLine('from typing import Optional', 0))
            all_lines.insert(1, PyLine('from decimal import Decimal', 0))
            all_lines.insert(2, PyLine('', 0))
            all_lines.insert(3, PyLine('', 0))
        for pyclass in self.classes:
            all_lines.extend(pyclass.get_lines())

        return [str(line) for line in all_lines]

