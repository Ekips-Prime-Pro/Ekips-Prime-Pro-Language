import customtkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from CTkMenuBar import CTkTitleMenu
import os
import sys
import shutil


class gui(tk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Text Editor")
        self.geometry("800x600")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Control-s>", self.save)
        # self.iconbitmap("icon.ico")
        self.main_programm()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            exit(0)    
            
    def save(self, event=None):
        pass
    
    def open(self):
        pass
    
    def main_programm(self):
        self.reset()
        self.CTkMenubar(self).add_menu("File")
        
    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    
        
class logik():
    def __init__(self):
        pass


if __name__ == "__main__":
    app = gui()
    app.mainloop()