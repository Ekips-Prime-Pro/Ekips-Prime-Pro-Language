import os
import sys
import shutil
import webbrowser as website

class compiler:
    def __init__(self):
        self.compile_register = [] # TODO: implement a register that stores the right order of the commands to compile
        self.compile_variables = [] # TODO: implement a register that stores the variables of the code
    
    def compile(self, file_path): #TODO: implement a compiler that compiles the .scsp file to a .py file and then to a .c file
        pass
    
    def reade_file(self, file_scsp):
        with open(file_scsp, "r") as file:
            content = file.read()
            for elment in content:
                elment = elment.readline()
                self.compile_register.append(elment)
            self.compile(elment) #TODO: implement a reading that is linear -> line by line
            
    def compile_to_py(self, file_path):
        # TODO: implement a the Text compiler that uses the compiler register to use the writable_content class
        if self.compile_register == []:
            self.reade_file(file_path)
        else:
            for element in self.compile_register:
                match element:
                    case "ai_supervised":
                        writable_content.ai_supervised()
                    case "ai_unsupervised":
                        writable_content.ai_unsupervised()
                    case "drive":
                        writable_content.drive()
                    case "ai_drive":
                        writable_content.ai_drive()
                    case "tank":
                        writable_content.tank()
                    case "ai_tank":
                        writable_content.ai_tank()
                    case "module":
                        writable_content.module()
                    case "wait":
                        writable_content.wait()
                    case "sensor":
                        writable_content.sensor()
                    case "calibrate":
                        writable_content.calibrate()
                    case "parallel":
                        writable_content.parallel()
    
    def compile_to_c(self, file_path):
        pass
                

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