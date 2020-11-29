import json
import argparse
import os

    
def get_data_from_file(path = None): 
# Функция используется для загрузки данных из файла.
# Если по указанному пути файл не открывается,
# функция будет запрашивать у пользователя правильный путь
    while True:
        if path == None: 
            path = input("Please, enter a new path to the file: ")
        try:
            with open(path) as file:
                json_data = json.loads(file.read())
                break;
        except IOError:
            print(f"File in {path} is not accessible, try another path")
            path = None
    return json_data


def get_initial_args():
    parser = argparse.ArgumentParser(description="Join students and rooms files")
    parser.add_argument("students", type=valid_path, help="Path to students file")
    parser.add_argument("rooms", type=valid_path, help="Path to rooms file")
    parser.add_argument("output", type=valid_type, help="Type of an output file")
    return parser.parse_args()


def valid_path(path):
    if not os.path.isfile(path):  
        raise argparse.ArgumentTypeError("Invalid path argument")
    else:
        return path


def valid_type(file_type):
    VALID_TYPES = ("XML", "JSON")
    if file_type.upper() not in VALID_TYPES:
        raise argparse.ArgumentTypeError("Invalid file format (choose XML or JSON)")        
    else:        
        return file_type