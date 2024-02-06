import os
import sys
import shutil

class compiler:
    def __init__(self):
        pass
    
    def compile(self, file_path):
        pass
    
    def run(self, file_path):
        try:
            os.system("cd dist")
            os.system(file_path)
            os.system("cd ..")
        except:
            return "Error while running file"
        return "File ran successfully"
    
    def delete(self, file_path):
        try:
            shutil.rmtree(file_path)
        except:
            return "Error while deleting file"
        return "File deleted successfully"
    
    def push(self):
        pass