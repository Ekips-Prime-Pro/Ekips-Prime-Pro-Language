import os
import sys
import shutil
import webbrowser as website

class compiler:
    def __init__(self):
        pass
    
    def compile(self, file_path): #TODO: implement a compiler that compiles the .scsp file to a .py file and then to a .c file
        pass
    
    def reade_file(self, file_scsp):
        with open(file_scsp, "r") as file:
            content = file.read()
            for elment in content:
                element.replace("\n", "")
                element.replace("\t", "")
                element.split(";")
                self.compile(elment) #TODO: implement a reading that is linear -> line by line
                

class cli: #TODO: implement a command line interface
    def __init__(self):
        input = ">>>"
        try:
            command, var = input.split(">")
        except:
            command = input
        if command == "exit":
            self.exit()
    
    def main(self):
        pass
    
    def help(self):
        pass
    
    def compile(self):
        pass
    
    def open(self):
        pass
    
    def save(self):
        pass
    
    def credits(self):
        pass
    
    def exit(self):
        sys.exit()
    
    def ask_file_path(self):
        pass
    
    def version(self):
        print("Version: 0.0.1")
    
    
class api: #TODO: implement an api for the main GUI
    def __init__(self):
        pass
    
    def open(self, file_path): #TODO: implement a file opener
        pass

class convert_to_C: #TODO: implement a converter
    def __init__(self):
        pass
    
    def convert(self, file_path):
        pass
    

class writable_content:#TODO: add the content of the functions in python
    def __init__(self):
        pass
    
    def ai(self): 
        pass
    
    def drive(self):
        pass
    
    def tank(self):
        pass
    
    def module(self):
        pass
    
    def wait(self):
        pass
    
    def sensor(self):
        pass
    
    def calibrate(self):
        pass
    
    def parallel(self):
        pass


