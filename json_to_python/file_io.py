import json

class FileIO:

    @staticmethod
    def read_file(file_name: str):
        with open(f'{file_name}.json') as f:
            data = json.load(f)
            return data

    @staticmethod
    def write_classes_to_file(out_file_name: str, lines: list[str]):
        with open(f'{out_file_name}.py', 'w') as f:
            f.writelines(lines)