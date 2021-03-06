import json
import xml.etree.cElementTree as ET
from abc import ABC, abstractmethod


class Writer(ABC):
    @abstractmethod
    def write(self, output_name, data):
        pass


class JsonWriter(Writer):
    def write(self, output_name, data):
        output_name += ".json"
        with open(output_name, "w") as file:
            json.dump(data, file, indent=2)


class XmlWriter(Writer):
    def write(self, output_name, data):
        # построение дерева для xml файла по строгой иерархии, с которой
        # в метод передается data и последующее сохранение дерева в файл
        output_name += ".xml"
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
        tree.write(output_name)


class WriterFactory():
    def __init__(self):
        self.types_dict = {
            "JSON": JsonWriter,
            "XML": XmlWriter
        }

    def create_writer(self, output_type) -> Writer:
        return self.types_dict[output_type]()


class DataDumper():
    def __init__(self, writer_factory: WriterFactory):
        self.writer_factory = writer_factory

    def dump_data(self, data, output_type, output_name=None):
        if output_name is not None:
            self.output_name = output_name
        else:
            self.output_name = "output"
        writer = self.writer_factory.create_writer(output_type)
        writer.write(output_name, data)
