import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import sys
import shutil
import webbrowser as website


class gui:
    def __init__(self):
        self.file = "N/A"
        self.root = tk.Tk()
        self.root.title("SCSaP") # Spike Custom System and Programming
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Control-s>", self.save())
        self.root.iconbitmap("icon.ico")
        self.main_programm()
        self.root.mainloop()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            exit(0)
            
    def save(self):
        try:
            file = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
            text = self.file_content.get()
            file.write(text)
            file.close()
        except:
            messagebox.showerror("Error", "Error while saving file")
    
    def open(self):
        content = logik.open()
        self.file_content.insert(tk.END, content)
        self.file = 
    
    def main_programm(self):
        if self.file == "N/A":
            self.file = "N/A"
        else:
            self.file = self.file
        tk.Label(self.root, text="File: ").place(x=150, y=0)
        tk.Label(self.root, text=self.file).place(x=170, y=0)
        self.file_content = tk.Text(self.root).place(x=150, y=20, relwidth=1, relheight=1)
        self.menu_top()
        self.toolbar()
        
    def licence(self):
        messagebox.showinfo("License", f"Path finding algorithm License Agreement\nThis License Agreement (the 'Agreement') is entered into by and between Maximilian Gründinger ('Licensor') and the First Lego League Team known as PaRaMeRoS ('Licensee').\n1. License Grant.\nLicensor hereby grants Licensee a non-exclusive, non-transferable license to use and modify the software program known as Algorithm Path Finding (the 'Program') solely for educational and non-commercial purposes. This license is granted exclusively to the members of the First Lego League Team identified as PaRaMeRoS.\n2. Restrictions.\nLicensee shall not, and shall not permit others to:\na. Use the Program for any purpose other than educational and non-commercial activities within the First Lego League Team.\nb. Allow non-members of the First Lego League Team to use or access the Program.\nc. Commercialize or distribute the Program for financial gain.\nd. Remove or alter any copyright, trademark, or other proprietary notices contained in the Program.\n3. Security.\nLicensor makes no warranties regarding the security of the Program. Licensee acknowledges and agrees that any use of the Program is at their own risk. Licensor shall not be responsible for any security bugs or issues that may arise in connection with the Program.\n4. Term and Termination.\nThis Agreement shall remain in effect until terminated by either party. Licensor reserves the right to terminate this Agreement immediately if Licensee breaches any of its terms. Upon termination, Licensee shall cease all use of the Program and destroy all copies in their possession.\n5. Disclaimer of Warranty.\nTHE PROGRAM IS PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. LICENSOR DISCLAIMS ALL WARRANTIES, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.\n6. Limitation of Liability.\nIN NO EVENT SHALL LICENSOR BE LIABLE FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM, EVEN IF LICENSOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.\n7. Governing Law.\nThis Agreement shall be governed by and construed in accordance with the laws of Germany, Bavaria, Munic.\n8. Entire Agreement.\nThis Agreement constitutes the entire agreement between the parties and supersedes all prior agreements, whether oral or written, with respect to the Program.\nIN WITNESS WHEREOF, the parties hereto have executed this License Agreement as of the effective date.\nLicensor:\nMaximilian Gründinger\nLicensee:\nPaRaMeRoS\nDate: 1.1.2024")
    
    def toolbar(self, mode=None):
        self.left_frame = tk.Frame(self.root, bg="white")
        self.left_frame.pack(side="left", fill="y")
        tk.Button(self.left_frame, text="Push", command=self.open, height=7, width=20).pack()
        tk.Button(self.left_frame, text="Update", command=self.save, height=7, width=20).pack()
        tk.Button(self.left_frame, text="help", command=self.save, height=7, width=20).pack()
        tk.Button(self.left_frame, text="Exit", command=self.on_closing, height=7, width=20).pack()
        
    def menu_top(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.file = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file)
        self.file.add_command(label="Open", command=self.open)
        self.file.add_command(label="Save", command=self.save)
        self.file.add_command(label="Save as", command=self.save)
        
        self.tools = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Tools", menu=self.tools)
        self.tools.add_command(label="Edit", command=self.open)
        self.tools.add_command(label="", command=self.save)
        self.tools.add_command(label="Save as", command=self.save)
        
        self.spike = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Spike", menu=self.spike)
        self.spike.add_command(label="Run", command=self.open)
        self.spike.add_command(label="Push", command=self.save)
        self.spike.add_command(label="Pull", command=self.save)
        self.spike.add_command(label="Update", command=self.save)
        
        self.help = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help)
        self.help.add_command(label="Credit", command=self.credit)
        self.help.add_command(label="License", command=self.licence)
        self.help.add_command(label="About", command=self.about)
        self.help.add_command(label="GitHub", command=self.github)
        self.help.add_command(label="Help/Dokumentation", command=self.help)
        
    def credit(self):
        messagebox.showinfo("Credit", "Maximilian Gründinger\nFirst Lego League Team PaRaMeRoS")
        
    def about(self):
        messagebox.showinfo("About", "Path finding algorithm\nVersion 1.0\nMaximilian Gründinger\nFirst Lego League Team PaRaMeRoS")
    
    def github(self):
        website.open("https://github.com/Iron-witch/Coding_lang_spike_PaRaMeRoS")
        
    def help(self):
        website.open("help.html")
        
    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    
        
class logik():
    def __init__(self):
        pass
    
    def open(self):
        file_name = filedialog.askopenfilename()
        return open(file_name, "r").read()

if __name__ == "__main__":
    gui()