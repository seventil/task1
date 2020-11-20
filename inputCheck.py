# -*- coding: utf-8 -*-
import json

class InputHandler():
    def __init__(self):
        pass
    
    def getPath(self, file):
        while True:
            path = input(f"Plaese, enter a path to the {file} file: ")
            try:
                with open(path) as a:
                    jsonData = json.loads(a.read())
                    break;
            except IOError:
                print(f"{file} file is not accessible, try another path")
        return jsonData
    
    def getOutput(self):
        while True:
            outputFormat = input("Please, enter an output file format (XML or JSON): ").upper()  
            if outputFormat.lower() == "xml" or outputFormat.lower() == "json":
                break;
            else:
                print("This is not a XML or JSON file format . Please enter a valid format")
        return outputFormat


