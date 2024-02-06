import os
import sys
import shutil

class compiler:
    def __init__(self):
        pass
    
    def compile(self, file_path): #TODO: implement a compiler that is linear
        pass
    
    def reade_file(self, file_scsp):
        with open(file_scsp, "r") as file:
            content = file.read()
            for elment in content:
                element.replace("\n", "")
                element.replace("\t", "")
                element.split(";")
                self.compile(elment) #TODO: implement a reading that is linear
                
                