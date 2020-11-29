import json
import xml.etree.cElementTree as ET
from abc import ABC, abstractmethod


class Writer(ABC):
# Интерфейс для взаимодействия класса FileDump с классами, записывающими данные
# в файл, в бд и т.п. с соотв. типом данных: XML, JSON и т.д.
    @abstractmethod
    def write(self, data):
        pass


class JsonWriter(Writer):
    def __init__(self, name):
        self.name = name
    def write(self, data):
        with open(self.name, "w") as file:
                json.dump(data, file, indent = 2)
    
    
class XmlWriter(Writer):
    def __init__(self, name):
        self.name = name
    def write(self, data):
        # построение дерева для xml файла по строгой иерархии, с которой
        # в метод передается data и последующее сохранение дерева в файл
        root = ET.Element("root")
        for room_data in data:     
            room_branch = ET.SubElement(root, "room")
            ET.SubElement(room_branch, "id").text = str(room_data["id"])
            ET.SubElement(room_branch, "name").text = room_data["name"]
            students_branch = ET.SubElement(room_branch, "students")
            for students_data in room_data["students"]:
                stud = ET.SubElement(students_branch, "student")
                ET.SubElement(stud, "id").text = str(students_data["id"])
                ET.SubElement(stud, "name").text = students_data["name"]
        tree = ET.ElementTree(root)
        tree.write(self.name) 


class DataDumper():
# Класс предназначен для того, чтобы записывать переданные данные в файл
# в соответствии с установленным форматом и названием файла
    def __init__(self, file_type, file_name=None):
        self.file_type = file_type
        # Если при инициализации объекта не было задано имя,
        # параметру file_name присваивается стандартное значение
        if file_name is not None:
            self.file_name = file_name
        else:
            self.file_name = "output"
        #Если в указанном имени не присутствует соотв. расширение,
        # оно добавляется автоматически
        if self.file_type.lower() not in self.file_name:
            self.file_name += "." + file_type.lower()
            
    def writer_selector(self):
    #метод, с помощью которого можно получить объект класса,
    #осуществляющего запись данных с соответствующим 
        TYPES_DICT = {"JSON":JsonWriter(self.file_name), "XML":XmlWriter(self.file_name)}
        return TYPES_DICT[self.file_type]
    
    def dump_data(self, data):
        writer = self.writer_selector()
        writer.write(data)
           