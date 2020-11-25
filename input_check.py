import json
import argparse

    
def check_data(file_to_open, path = None): 
#метод используется для загрузки данных из файла. Если метод был вызван без указания пути или с неправильно
#указанным путем файла, метод будет запрашивать у пользователя правильный путь
    while True:
        if path == None: 
            path = input(f"Please, enter a path to the {file_to_open} file: ")
        try:
            with open(path) as file:
                json_data = json.loads(file.read())
                break;
        except IOError:
            print(f"{file_to_open} file is not accessible, try another path")
            path = None
    return json_data

def check_output(output_format = None):
#метод используется для проверки правильного указания формата файла. Если формат не указан или указан неправильно
#метод будет запрашивать у пользователя подходящее название
    while True:
        if output_format == None:
            output_format = input("Please, enter an output file format: ")
        if output_format.upper() == "XML" or output_format.upper() == "JSON":
            break;
        else:
            print("File format is invalid. Please, enter another file format")
            output_format = None
    return output_format

def get_initial_args():
    parser = argparse.ArgumentParser(description="Join students and rooms files")
    parser.add_argument("students", help="Path to students file")
    parser.add_argument("rooms", help="Path to rooms file")
    parser.add_argument("output", help="Type of an output file")
    return parser.parse_args()

    