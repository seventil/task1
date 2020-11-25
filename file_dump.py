import json
import xml.etree.cElementTree as ET


class FileDump():
# Класс предназначен для того, чтобы записывать переданные данные в файл
# в соответствии с установленным форматом и названием файла

    def __init__(self, file_type, file_name=None):
        self.file_type = file_type
        # Если при инициализации объекта не было задано имя,
        # параметру file_name присваивается стандартное значение
        if file_name not None:
            self.file_name = file_name
        else:
            self.file_name = "output"
        #Если в указанном имени не присутствует соотв. расширение,
        # оно добавляется автоматически
        if self.file_type.lower() not in self.file_name:
            self.file_name += "." + file_type.lower()
       
    def write_to_file(self, data): 
    # метод, записывающий в файл данные, переданные с data,
    # в соответствии с заданными в объекте file_type и file_name       
        if self.file_type == "JSON":
            # сохранение в json файл
            with open(self.file_name, "w") as file:
                json.dump(data, file, indent = 2)                            
        elif self.file_type == "XML":
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
            tree.write(self.file_name)
