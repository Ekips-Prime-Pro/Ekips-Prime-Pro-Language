import os
import sys
import shutil
import webbrowser as website

class compiler:
    def __init__(self):
        self.compile_register = []
    
    def compile(self, file_path): #TODO: implement a compiler that compiles the .scsp file to a .py file and then to a .c file
        pass
    
    def reade_file(self, file_scsp):
        with open(file_scsp, "r") as file:
            content = file.read()
            for elment in content:
                elment = elment.readline()
                self.compile_register.append(elment)
            self.compile(elment) #TODO: implement a reading that is linear -> line by line
                

class cli: #TODO: implement a command line interface
    def __init__(self):
        while True:
            print("enter a command:")
            input = ">>>"
            try:
                command, var = input.split(">")
            except:
                command = input
            if command == "exit":
                self.exit()
            elif command == "open":
                self.open()
            elif command == "save":
                self.save()
            elif command == "compile":
                self.compile()
            elif command == "help":
                self.help()
            elif command == "credits":
                self.credits()
            elif command == "version":
                self.version()

    
    def help(self):
        print("Commands: ")
    
    def compile(self):
        pass
    
    def open(self):
        pass
    
    def save(self):
        pass
    
    def credits(self):
        print("Credits: Maximilian Gründinger")
        print("@AIIrondev, 2024")
        print("All rights reserved")
    
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
    
    def ai_supervised(self): 
        pass
    
    def ai_unsupervised(self):
        pass
    
    def drive(self):
        pass
    
    def ai_drive(self):
        pass
    
    def tank(self):
        pass
    
    def ai_tank(self):
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


if __name__ == "__main__":
    cli()