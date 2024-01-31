import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import sys
import shutil


class gui(tk.Tk):
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
        menu_bar = tk.Menu(self, bg="white", fg="black")
        menu_bar.add_command(label="Open", command=self.open)
        menu_bar.add_command(label="Save", command=self.save)
        menu_bar.add_command(label="Save as", command=self.save)
        menu_bar.add_command(label="Exit", command=self.on_closing)
        menu_bar.add_cascade(label="File", menu=menu_bar)
        self.config(menu=menu_bar)
        
    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    
        
class logik():
    def __init__(self):
        pass


if __name__ == "__main__":
    app = gui()
    app.mainloop()