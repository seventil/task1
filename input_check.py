import json


class InputHandler():
#Класс, который предназначен для обработки входных параметров. Проверит указан ли формат данных или путь
#или был указан правильно, если нет - будет запрашивать путь от пользователя
    def __init__(self):
        pass  
    
    def getData(self, file, path = None): 
    #метод используется для загрузки данных из файла. Если метод был вызван без указания пути или с неправильно
    #указанным путем файла, метод будет запрашивать у пользователя правильный путь
        while True:
            if path == None: 
                path = input(f"Plaese, enter a path to the {file} file: ")
            try:
                with open(path) as a:
                    jsonData = json.loads(a.read())
                    break;
            except IOError:
                print(f"{file} file is not accessible, try another path")
                path = None
        return jsonData
    
    def getOutput(self, outputFormat = None):
    #метод используется для проверки правильного указания формата файла. Если формат не указан или указан неправильно
    #метод будет запрашивать у пользователя подходящее название
        while True:
            if outputFormat == None:
                outputFormat = input("Please, enter an output file format (XML or JSON): ").upper()  
            if outputFormat.lower() == "xml" or outputFormat.lower() == "json":
                break;
            else:
                print("This is not a XML or JSON file format . Please enter a valid format")
                outputFormat = None
        return outputFormat
    