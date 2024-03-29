from .naming import Naming
from .file_io import FileIO
from .pyclass import PyClass, PyClassList


class JsonToPython:

    @staticmethod
    def dict_to_class(data: dict, name: str, classes: PyClassList) -> PyClassList:
        pyclass = PyClass(name)
        pyclass.add_line(f'class {pyclass.class_name}:', 0)
        data_dict_name = f'{pyclass.snake_case_name}_data'
        pyclass.add_line(f'def __init__(self, {data_dict_name}: dict):', 1)
        for key, val in data.items():
            class_property_name = Naming.camel_to_snake(key)
            # Can't have dashes
            class_property_name = class_property_name.replace('-', '_')
            if type(val) is float:
                pyclass.import_decimal = True
                pyclass.add_line(f"{class_property_name}: float = {data_dict_name}.get('{key}')", 2)
                pyclass.add_line(
                        f"self.{class_property_name}: Optional[Decimal] = Decimal(str({class_property_name})) if {class_property_name} is not None else None",
                        2
                )
            elif type(val) is list:
                if val:
                    if type(val[0]) is float:
                        pyclass.import_decimal = True
                        pyclass.add_line(f"self.{class_property_name}: list[Decimal] = [Decimal(str(item)) for item in {data_dict_name}.get('{key}')]", 2)
                    if type(val[0]) is dict:
                        last_class = JsonToPython.dict_to_class(val[0], key, classes).get_last_class()
                        pyclass.add_line(f"self.{class_property_name}: list[{last_class.class_name}] = [{last_class.class_name}(item) for item in {data_dict_name}.get('{key}')]", 2)
                    else:
                        type_label = type(val).__name__
                        pyclass.add_line(f"self.{class_property_name}: list[{type_label}] = {data_dict_name}.get('{key}')", 2)
                else:
                    pyclass.add_line(f"self.{class_property_name}: list = {data_dict_name}.get('{key}')", 2)
            elif type(val) is dict:
                last_class = JsonToPython.dict_to_class(val, key, classes).get_last_class()
                sub_class_data_name = f'{class_property_name}_data'
                pyclass.add_line(f"{sub_class_data_name}: dict = {data_dict_name}.get('{key}')", 2)
                pyclass.add_line(f"self.{class_property_name}: {last_class.class_name} = {last_class.class_name}({sub_class_data_name}) if {sub_class_data_name} is not None else None", 2)
            else:
                type_label = type(val).__name__
                pyclass.add_line(f"self.{class_property_name}: {type_label} = {data_dict_name}.get('{key}')", 2)

        pyclass.add_line('', 0)
        pyclass.add_line(f'def __dict__(self):', 1)
        pyclass.add_line(f'return {{', 2)
        for key, val in data.items():
            class_property_name = Naming.camel_to_snake(key)
            # Can't have dashes in python naming
            class_property_name = class_property_name.replace('-', '_')
            if type(val) is list:
                if val:
                    if type(val[0]) is float:
                        pyclass.add_line(f"'{key}': [str(item) for item in self.{class_property_name}],", 3)
                    if type(val[0]) is dict:
                        pyclass.add_line(f"'{key}': [item.__dict__ for item in self.{class_property_name}],", 3)
                    else:
                        pyclass.add_line(f"'{key}': self.{class_property_name},", 3)
                else:
                    pyclass.add_line(f"'{key}': self.{class_property_name},", 3)
            elif type(val) is dict:
                pyclass.add_line(f"'{key}': self.{class_property_name}.__dict__,", 3)
            else:
                pyclass.add_line(f"'{key}': self.{class_property_name},", 3)
        pyclass.add_line(f'}}', 2)

        pyclass.add_line('', 0)
        pyclass.add_line('', 0)

        classes.add_class(pyclass)
        return classes

    @staticmethod
    def transform_file(name: str):
        data = FileIO.read_file(name)
        classes = JsonToPython.dict_to_class(data, name, PyClassList())
        FileIO.write_classes_to_file(name, classes.get_line_strings())
