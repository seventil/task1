# -*- coding: utf-8 -*-
import json
import xml.etree.cElementTree as ET

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
            name = name + ".xml"
            root = ET.Element("root")
            for i in data:     
                room = ET.SubElement(root, "room")
                ET.SubElement(room, "id").text = str(i["id"])
                ET.SubElement(room, "name").text = i["name"]
                students = ET.SubElement(room, "students")
                for k in i["students"]:
                    stud = ET.SubElement(students, "student")
                    ET.SubElement(stud, "id").text = str(k["id"])
                    ET.SubElement(stud, "name").text = k["name"]
            tree = ET.ElementTree(root)
            tree.write(name)
            
                
        
    
