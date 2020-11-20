# -*- coding: utf-8 -*-
import json

class FileDump():
# Класс, при инициализации объекта которого через входной параметр fileType определяется формат выходного файла
# Предназначен для того, чтобы записывать переданные данные в файл в соответствии с установленным форматом файла
    def __init__(self, fileType):
        self.fileType = fileType
        
    def writeFile(self, name, data):
        
        if self.fileType == "JSON":
            name = name + ".json"
            with open(name, "w") as f:
                json.dump(data, f, indent = 2)
                
        if self.fileType == "XML":
            print("XML not realised!")
                
        
    
