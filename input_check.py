import json
import argparse

    
def checkData(file_to_open, path = None): 
#метод используется для загрузки данных из файла. Если метод был вызван без указания пути или с неправильно
#указанным путем файла, метод будет запрашивать у пользователя правильный путь
    while True:
        if path == None: 
            path = input(f"Please, enter a path to the {file_to_open} file: ")
        try:
            with open(path) as a:
                jsonData = json.loads(a.read())
                break;
        except IOError:
            print(f"{file_to_open} file is not accessible, try another path")
            path = None
    return jsonData

def checkOutput(outputFormat = None):
#метод используется для проверки правильного указания формата файла. Если формат не указан или указан неправильно
#метод будет запрашивать у пользователя подходящее название
    while True:
        if outputFormat == None:
            outputFormat = input("Please, enter an output file format: ").upper()  
        if outputFormat.lower() == "xml" or outputFormat.lower() == "json":
            break;
        else:
            print("File format is invalid. Please, enter another file format")
            outputFormat = None
    return outputFormat

def get_initial_args():
    parser = argparse.ArgumentParser(description="Join students and rooms files")
    parser.add_argument("students", help="Path to students file")
    parser.add_argument("rooms", help="Path to rooms file")
    parser.add_argument("output", help="Type of an output file")
    return parser.parse_args()

    