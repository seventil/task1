# -*- coding: utf-8 -*-
import json

while True:
    studentsPath = input("Plaese, enter a path to the students file: ")
    try:
        with open(studentsPath) as a:
            students = json.loads(a.read())
            break;
    except IOError:
        print("Students file is not accessible, try another path")
        
while True:  
    roomsPath = input("Plaese, enter a path to the rooms file: ")
    try:
        with open(roomsPath) as b:
            rooms = json.loads(b.read())
            break;
    except IOError:
        print("Rooms file is not accessible, try another path")

while True:    
    outputFormat = input("Please, enter an output file format (XML or JSON): ").upper()  
    if outputFormat.lower() == "xml" or outputFormat.lower() == "json":
        break;
    else:
        print("This is not a XML or JSON file format . Please enter a valid format")
