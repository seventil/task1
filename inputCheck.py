# -*- coding: utf-8 -*-
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
    
    
    
class InitialDataHandler():
#Класс, который должен при инициализации объекта должен обработать полученные на вход аргументы (например, sys.argv),
#которые представляют собой последовательность: название файла, путь к студентам, путь к комнатам, название файла на выход
#используя соответствующие методы, можно получить лист для студентов, лист для комнат и строку формат файла
    def __init__(self, args):
    #интересующие нас пераргументы изначально приравниваются к None или присваиваются из args, если они там указаны
    #работает только со строгой последовательностью в args: [1] - путь к студентам, [2] - путь к комнатам,
    #[3] - формат файла на выходе
        self.studentPath = None
        self.roomsPath = None
        self.dataFormat = None
        self.ih = InputHandler()
        self.args = args
        self.l = len(args)
        if self.l > 1:
            self.studentPath = self.args[1]
        if self.l > 2:
            self.roomsPath = self.args[2]
        if self.l > 3:
            self.dataFormat = self.args[3]
                       
    def getStudents(self):
        return self.ih.getData("students", self.studentPath)
    
    def getRooms(self):
        return self.ih.getData("rooms", self.roomsPath)
    
    def getOutputFormat(self):
        return self.ih.getOutput(self.dataFormat)