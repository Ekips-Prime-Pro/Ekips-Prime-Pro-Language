#TODO: add customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from customtkinter import *
import os
import sys
import shutil
import webbrowser as website

#TODO: remove global variables
global file_name
global file_content
file_name = "N/A"
file_content = "N/A"

class gui:
    def __init__(self):
        self.langs = ["English", "German"]
        self.lang = "N/A"
        self.file = "N/A"
        self.file_content = "N/A"
        self.app = CTk()
        self.app.title("Spike Prime Custom System Programming") # File extension .scsp
        self.app.geometry("800x600")
        self.app.resizable(True, True)
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app.iconbitmap("icon.ico")
        self.setup()
        self.main_programm()
        self.app.mainloop()

    def setup(self):
        self.app.withdraw()

        self.setup = CTkToplevel(self.app)
        self.setup.title("Spike Prime Custom System Programming Setup")
        self.setup.geometry("300x400")
        self.setup.resizable(False, False)
        self.setup.iconbitmap("icon.ico")
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.setup_Title1 = CTkLabel(self.setup, text="Setup", font=("Arial", 60))
        self.setup_Title2 = CTkLabel(self.setup, text="Program", font=("Arial", 60))
        self.setup_lang_lable = CTkLabel(self.setup, text="Language:", font=("Arial", 25))
        self.setup_lang = CTkComboBox(self.setup, values=self.langs, font=("Arial", 20), corner_radius=20, border_width=0, dropdown_font=("Arial", 20))
        self.setup_submit = CTkButton(self.setup, text="Submit Settings", command=self.submit, font=("Arial", 30), corner_radius=20, border_width=0)

        self.setup_Title1.place(relx=0.5, rely=0.15, anchor="center")
        self.setup_Title2.place(relx=0.5, rely=0.3, anchor="center")
        self.setup_lang_lable.place(relx=0.5, rely=0.55, anchor="center")
        self.setup_lang.place(relx=0.5, rely=0.65, anchor="center")
        self.setup_submit.place(relx=0.5, rely=0.9, anchor="center")

    def submit(self):
        self.lang = self.setup_lang.get()
        self.setup.destroy()
        self.app.deiconify()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.app.destroy()
            exit(0)
            
    def save(self):
        if self.file == "N/A":
            Files = [('Spike Custom System Programming', '*.scsp'), ('Text Document', '*.txt')]
            file = filedialog.asksaveasfile(filetypes = Files, defaultextension = Files)
            if file is not None:
                if self.file_author == "N/A":
                    self.file_author = os.system("whoami")
                file.write("<Author>" + self.file_author + "</Author>")
                file.write(self.file_content.get("1.0", "end-1c"))
                file.close()
            file = file.name
            self.file_label.config(text=f"File: {file}")
        else:
            with open(self.file, "w") as f:
                f.write("<Author>" + self.file_author + "</Author>")
                f.write(self.file_content.get("1.0", "end-1c"))
    
    def push(self):
        # TODO: add the push.py file API
        pass
    
    def pull(self):
        pass
    
    def update_gui(self):
        # TODO: add the update.py class
        yes = messagebox.askyesno("Update", "Do you want to update the programm?")
        if yes:
            os.system("update_gui.bat")
            exit(0)
        else:
            messagebox.showinfo("Update", "The programm will not be updated")
        
    def update_spike(self):
        yes = messagebox.askyesno("Update", "Do you want to update the Spike Operating System?")
        if yes:
            os.system("update_spike.bat")
        else:
            messagebox.showinfo("Update", "The Spike Operating System will not be updated")
    
    def open(self):
        try:
            if self.file_content.get("1.0", "end-1c") != "": #TODO: add a messagebox to ask if the user want to save the file
                msg = messagebox.askyesno("Save", "Do you want to save the file?")
                if msg:
                    self.save()
                else:
                    pass
            file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Spike Custom System Programming", "*.scsp")])
            self.file_label.config(text=f"File: {file}")
            with open(file, "r") as f:
                def delete_line(s, line_num):
                    lines = s.splitlines()
                    if line_num < len(lines):
                        del lines[line_num]
                    return '\n'.join(lines)  
                Author = f.readline(1)
                Author = Author.replace("<Author>", "")
                Author = Author.replace("</Author>", "")
                self.file_author.config(text=f"Author: {Author}")
                # TODO:Delete the Author tag from the str and just let the file_content be the content of the str
                content = f.readlines()
                content = delete_line(content, 0)
                self.file_content.delete("1.0", "end")
                self.file_content.insert("1.0", f.read())
        except:
            messagebox.showerror("Error", "Error while opening file")
    
    def main_programm(self):
        self.file_label = CTkLabel(self.app, text="File: N/A")
        self.file_author = CTkLabel(self.app, text="Author: N/A")
        self.file_label.place(x=150, y=0)
        self.file_author.place(x=220, y=0)
        self.file_content = tk.Text(self.app)
        self.file_content.place(x=150, y=20, relwidth=1, relheight=1)
        self.menu_top()
        self.toolbar()

    def licence(self):
        messagebox.showinfo("License", f"Spike Custom System Programming License Agreement\nThis License Agreement (the 'Agreement') is entered into by and between Maximilian Gründinger ('Licensor') and the First Lego League Team known as PaRaMeRoS ('Licensee').\n1. License Grant.\nLicensor hereby grants Licensee a non-exclusive, non-transferable license to use and modify the software program known as Spike Custom System Programming (the 'Program') solely for educational and non-commercial purposes. This license is granted exclusively to the members of the First Lego League Team identified as PaRaMeRoS.\n2. Restrictions.\nLicensee shall not, and shall not permit others to:\na. Use the Program for any purpose other than educational and non-commercial activities within the First Lego League Team.\nb. Allow non-members of the First Lego League Team to use or access the Program.\nc. Commercialize or distribute the Program for financial gain.\nd. Remove or alter any copyright, trademark, or other proprietary notices contained in the Program.\n3. Security.\nLicensor makes no warranties regarding the security of the Program. Licensee acknowledges and agrees that any use of the Program is at their own risk. Licensor shall not be responsible for any security bugs or issues that may arise in connection with the Program.\n4. Term and Termination.\nThis Agreement shall remain in effect until terminated by either party. Licensor reserves the right to terminate this Agreement immediately if Licensee breaches any of its terms. Upon termination, Licensee shall cease all use of the Program and destroy all copies in their possession.\n5. Disclaimer of Warranty.\nTHE PROGRAM IS PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. LICENSOR DISCLAIMS ALL WARRANTIES, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.\n6. Limitation of Liability.\nIN NO EVENT SHALL LICENSOR BE LIABLE FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM, EVEN IF LICENSOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.\n7. Governing Law.\nThis Agreement shall be governed by and construed in accordance with the laws of Germany, Bavaria, Munic.\n8. Entire Agreement.\nThis Agreement constitutes the entire agreement between the parties and supersedes all prior agreements, whether oral or written, with respect to the Program.\nIN WITNESS WHEREOF, the parties hereto have executed this License Agreement as of the effective date.\nLicensor:\nMaximilian Gründinger\nLicensee:\nPaRaMeRoS\nDate: 1.1.2024")
    
    def toolbar(self, mode=None):
        self.left_frame = CTkFrame(self.app)
        self.left_frame.pack(side="left", fill="y")
        CTkButton(self.left_frame, text="Push", command=self.push, height=7, width=20).pack()
        CTkButton(self.left_frame, text="Update", command=self.update_spike, height=7, width=20).pack()
        CTkButton(self.left_frame, text="help", command=self.help_web, height=7, width=20).pack()
        CTkButton(self.left_frame, text="Exit", command=self.on_closing, height=7, width=20).pack()
        
    def debug(self):
        messagebox.showinfo("Debug", "Debugging is not available in this version this will be added in a later version.")    
        #TODO: add the debug system with the API of the Spike Custom Programming

    #TODO: Make Custom Menu
    def menu_top(self):
        pass
        #self.menu = tk.Menu(self.app)
        #self.app.config(menu=self.menu)
        #self.file = tk.Menu(self.menu, tearoff=0)
        #self.menu.add_cascade(label="File", menu=self.file)
        #self.file.add_command(label="Open", command=self.open)
        #self.file.add_command(label="Save", command=lambda: self.save())
        #self.file.add_command(label="Save as", command=self.save)
        #self.file.add_command(label="Rename Author", command=self.name_author)
        #
        #self.tools = tk.Menu(self.menu, tearoff=0)
        #self.menu.add_cascade(label="Tools", menu=self.tools)
        #self.menu.add_command(label="Debug", command=self.debug)
        #self.tools.add_command(label="Compile", command=self.compile)
        #self.tools.add_command(label="Pull", command=self.pull)
        #
        #self.spike = tk.Menu(self.menu, tearoff=0)
        #self.menu.add_cascade(label="Spike", menu=self.spike)
        #self.spike.add_command(label="Run", command=self.open)
        #self.spike.add_command(label="Push", command=self.push)
        #self.spike.add_command(label="Pull", command=self.pull)
        #self.spike.add_command(label="Update", command=self.update_spike)
        #
        #self.usb = tk.Menu(self.menu, tearoff=0)
        #self.wireless = tk.Menu
        #self.menu.add_cascade(label="Connect", menu=self.usb)
        #self.usb.add_command(label="USB", command=self.usb_connection)
        #self.usb.add_command(label="Wireless", command=self.usb_connection)
        #
        #
        #self.help = tk.Menu(self.menu, tearoff=0)
        #self.menu.add_cascade(label="Help", menu=self.help)
        #self.help.add_command(label="Credit", command=self.credit)
        #self.help.add_command(label="License", command=self.licence)
        #self.help.add_command(label="About", command=self.about)
        #self.help.add_command(label="GitHub", command=self.github)
        #self.help.add_command(label="Help/Dokumentation", command=self.help_web)
        #self.help.add_command(label="Update", command=self.update_gui)
        
    def name_author(self):
        self.author = tk.Tk()
        self.author.title("Rename Author")
        self.author.geometry("300x100")
        self.author.resizable(False, False)
        self.author.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.label = CTkLabel(self.author, text="Enter your name:")
        self.label.pack()
        self.entry = CTkEntry(self.author)
        self.entry.pack()
        self.button = CTkButton(self.author, text="Rename", command=self.rename)
        self.button.pack()
    
    def rename(self):
        self.author_name = self.entry.get()
        self.file_author.config(text=f"Author: {self.author_name}")
        self.author.destroy()
    
    def credit(self):
        messagebox.showinfo("Credit", "Maximilian Gründinger\nFirst Lego League Team PaRaMeRoS")
        
    def about(self):
        messagebox.showinfo("About", "Spike Custom System Programming\nVersion 0.0.1\nMaximilian Gründinger\nFirst Lego League Team PaRaMeRoS")
    
    def github(self):
        website.open("https://github.com/Iron-witch/Coding_lang_spike_PaRaMeRoS")
        
    def help_web(self):
        messagebox.showinfo("Help", "For help and documentation please visit the GitHub page of the project")
        website.open("https://github.com/Iron-witch/Coding_lang_spike_PaRaMeRoS/wiki")
        
    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    def compile(self): # TODO: add the compiler install and run command
        pass
    
    def usb_connection(self): #TODO: add the usb_connection system
        pass


class update(mode):
    def __init__(self):
        pass
    
    def update_gui(self):
        pass
    
    def update_spike(self):
        pass


class connect(mode):
    def __init__(self):
        pass
    
    def usb_connection(self):
        pass
    
    def wireless_connection(self):
        pass


class compiler(mode):
    def __init__(self):
        pass
    
    def compile(self):
        pass
    
    def debug(self):
        pass
    
    
class tools(mode, projekt):
    def __init__(self):
        pass
    
    def pull(self):
        pass
    
    def push(self):
        pass


if __name__ == "__main__":
    gui()
