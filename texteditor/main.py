import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import sys
import shutil


class gui:
    def __init__(self):
        root = tk.Tk()
        root.title("SCSaP") # Spike Custom System and Programming
        root.geometry("800x600")
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        root.bind("<Control-s>", self.save)
        # self.iconbitmap("icon.ico")
        self.main_programm()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            exit(0)
            
    def save(self):
        pass
    
    def open(self):
        pass
    
    def main_programm(self):
        tk.Button(root, text="LICENSE", command=self.licence)
        self.menu_top()
        
    def licence(self):
        tk2.messagebox.showinfo("License", f"Path finding algorithm License Agreement\nThis License Agreement (the 'Agreement') is entered into by and between Maximilian Gründinger ('Licensor') and the First Lego League Team known as PaRaMeRoS ('Licensee').\n1. License Grant.\nLicensor hereby grants Licensee a non-exclusive, non-transferable license to use and modify the software program known as Algorithm Path Finding (the 'Program') solely for educational and non-commercial purposes. This license is granted exclusively to the members of the First Lego League Team identified as PaRaMeRoS.\n2. Restrictions.\nLicensee shall not, and shall not permit others to:\na. Use the Program for any purpose other than educational and non-commercial activities within the First Lego League Team.\nb. Allow non-members of the First Lego League Team to use or access the Program.\nc. Commercialize or distribute the Program for financial gain.\nd. Remove or alter any copyright, trademark, or other proprietary notices contained in the Program.\n3. Security.\nLicensor makes no warranties regarding the security of the Program. Licensee acknowledges and agrees that any use of the Program is at their own risk. Licensor shall not be responsible for any security bugs or issues that may arise in connection with the Program.\n4. Term and Termination.\nThis Agreement shall remain in effect until terminated by either party. Licensor reserves the right to terminate this Agreement immediately if Licensee breaches any of its terms. Upon termination, Licensee shall cease all use of the Program and destroy all copies in their possession.\n5. Disclaimer of Warranty.\nTHE PROGRAM IS PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. LICENSOR DISCLAIMS ALL WARRANTIES, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.\n6. Limitation of Liability.\nIN NO EVENT SHALL LICENSOR BE LIABLE FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM, EVEN IF LICENSOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.\n7. Governing Law.\nThis Agreement shall be governed by and construed in accordance with the laws of Germany, Bavaria, Munic.\n8. Entire Agreement.\nThis Agreement constitutes the entire agreement between the parties and supersedes all prior agreements, whether oral or written, with respect to the Program.\nIN WITNESS WHEREOF, the parties hereto have executed this License Agreement as of the effective date.\nLicensor:\nMaximilian Gründinger\nLicensee:\nPaRaMeRoS\nDate: 1.1.2024")
    
    def toolbar(self, mode=None):
        if event == "File":
            self.left_frame = tk.Frame(self, bg="white")
            self.left_frame.pack(side="left", fill="y")
            tk.Button(self.left_frame, text="Open", command=self.open).pack()
            tk.Button(self.left_frame, text="Save", command=self.save).pack()
            tk.Button(self.left_frame, text="Save as", command=self.save).pack()
            tk.Button(self.left_frame, text="Exit", command=self.on_closing).pack()
        elif event == "tools":
            self.left_frame.destroy()
            self.left_frame = tk.Frame(self, bg="white")
            self.left_frame.pack(side="left", fill="y")
            tk.Button(self.left_frame, text="Open", command=self.open).pack()
        else:
            self.left_frame.destroy()
        
        
        
    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    
        
class logik():
    def __init__(self):
        pass


if __name__ == "__main__":
    app = gui()
    app.mainloop()