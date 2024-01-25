import customtkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import sys
import shutil


class gui(tk.TK):
    def __init__(self):
        super().__init__()
        self.title("Text Editor")
        
        
        
class logik():
    def __init__(self):
        self.file = None
        self.filepath = None
        self.filename = None
        self.filetype = None
        self.filecontent = None
        self.filecontent_old = None
        
    def generate_file(self, filepath, filename):
        self.file = open(os.path.join(filepath, f"{filename}.f"), "w")
        self.file.close()
        
    def open_file(self, filepath, filename):
        self.file = open(os.path.join(filepath, filename), "r")
        self.filecontent = self.file.read()
        self.filecontent_old = self.filecontent
        self.file.close()