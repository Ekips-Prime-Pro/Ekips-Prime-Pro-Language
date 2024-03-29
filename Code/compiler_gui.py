# Imports
import webbrowser as website
import customtkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import sys

# Variables
content_compile = []
__version__ = "0.0.0.0"

with open("version", "r") as f:
    __version__ = f.read()

# Functions
def compile(file):
    """
    Compiles the given file if it has a valid extension (.scsp).
    
    Parameters:
        file (str): The path of the file to compile.
    """
    print(f"Compiling {file}...")
    if file.endswith(".scsp"):
        with open(file, "r") as f:
            content = f.readlines()
            for line in content:
                content_compile.append(line)
    else:
        print(f"Error: The file {file} is not a valid file type.")

def get_active_function(line):
    """
    Extracts the active function and its value from a line.
    
    Parameters:
        line (str): The line to extract the function from.
    
    Returns:
        tuple: A tuple containing the function and its value.
    """
    content_line = line
    function, variable = content_line.split("{")
    variable = variable.replace("{","")
    variable = variable.replace("}","")
    variable = variable.replace("\n","")
    return function, variable
    
def write_function(function,file,value=False):
    """
    Writes the specified function and its value to a Python file.
    
    Parameters:
        function (str): The function to write.
        file (str): The name of the file to write to.
        value (str, optional): The value associated with the function. Defaults to False.
    """
    print(f"Writing {function} function...")
    file_name = file.split(".")
    file_name = file_name[0]
    with open(f"{file_name}.py", "a") as f:
        match function:
            case "log":
                print_out = f"print('{str(value)}')\n"
                f.write(print_out)
            case "sleep":
                sleep_out = f"time.sleep({str(value)})\n"
                f.write(sleep_out)
            case "init":
                init_out = f"import force_sensor, distance_sensor, motor, motor_pair\nfrom hub import port\nimport time\nfrom app import linegraph as ln\nimport runloop\nfrom math import *\nimport random\n"
                f.write(init_out)
            case "ai.chose":
                ai_chose_out = f"ai_chose = '{str(value)}'\n"
                f.write(ai_chose_out)
            case "ai.init":
                ai_init_out = f"ai = runloop.AI()\n"
                f.write(ai_init_out)
                with open("ai.fll", "r") as r:
                    ai_content = r.readlines()
                    for line in ai_content:
                        f.write(line)
            case "module.init":
                with open("module.fll", "r") as r:
                    ai_content = r.readlines()
                    for line in ai_content:
                        f.write(line)
            case "motor.init":
                with open("motor.fll", "r") as r:
                    ai_content = r.readlines()
                    for line in ai_content:
                        f.write(line)
            case "sensor.init":
                with open("sensor.fll", "r") as r:
                    ai_content = r.readlines()
                    for line in ai_content:
                        f.write(line)
            case "calibration.init":
                with open("calibration.fll", "r") as r:
                    ai_content = r.readlines()
                    for line in ai_content:
                        f.write(line)
            case "variables.init":
                with open("variables.fll", "r") as r:
                    ai_content = r.readlines()
                    for line in ai_content:
                        f.write(line)
            case "drive":
                f.write(f"  await drive({value})\n")
            case "tank":
                f.write(f"  await tank({value})\n")
            case "obstacle":
                f.write(f"  await obstacle({value})\n")
            case "ai.sensor":
                # add the sensor to the ai input
                f.write(f"ai_sensor.append('{value}\n')")
            case "module":
                f.write(f"  await module({value})\n")
            case "calibrate":
                f.write("   await calibrate()\n")
            case "ai.data_save":
                f.write(f"  write_ai_data('{value}')\n")
            case "ai.data_load":
                for line in value:
                    f.write(f"ai_data.append({line})\n")
            case "main.init":
                f.write("async def main():\n")
            case "main.run":
                f.write("runloop.run(main())\n")
            case _:
                if function == "//":
                    f.write(f"# {value}")
                elif function == "#":
                    f.write(f"# {value}")
                else:
                    print(f"Error: The function {function} does not exist.")
                    sys.exit(1)

def debug_function(function,value=False):
    """
    Debugs the specified function.
    
    Parameters:
        function (str): The function to debug.
        value (str, optional): The value associated with the function. Defaults to False.
    """
    print(f"Debuging {function} function...")
    match function:
        case "log":
            pass
        case "sleep":
            check_for_format("int", value)
        case "init":
            pass
        case "ai.chose":
            value = f"{value}"
            match value:
                case "supervised":
                    pass
                case "unsupervised":
                    pass
                case "deep_learning":
                    pass
                case _:
                    messagebox.askokcancel(f"Error: The AI {value} does not exist.")
                    exit(1)
        case "ai.init":
            pass
        case "module.init":
            pass
        case "motor.init":
            pass
        case "sensor.init":
            pass
        case "calibration.init":
            pass
        case "variable.init":
            pass
        case "drive":
            check_for_format("int", value)
        case "tank":
            check_for_format("int", value)
        case "obstacle":
            check_for_format("int", value)
        case "ai.sensor":
            value = f"{value}"
            match value:
                case "force":
                    pass
                case "distance":
                    pass
                case "color":
                    pass
                case "gyro":
                    pass
                case _:
                    messagebox.askokcancel(f"Error: The sensor {value} does not exist.")
                    exit(1)
        case "module":
            check_for_format("int", value)
        case "calibrate":
            pass
        case "ai.data_save":
            pass
        case "ai.data_load":
            pass
        case "main.init":
            pass
        case "main.run":
            pass
        case _:
            if function == "//":
                pass
            elif function == "#":
                pass
            else:
                print(f"Error: The function {function} does not exist.")
                sys.exit(1)
            
def main_debug(file):
    """
    Main function for debugging the compiled file.
    
    Parameters:
        file (str): The name of the file to debug.
    """
    for line in content_compile:
        # Komentare herausfiltern
        function, value = get_active_function(line)
        debug_function(function, value)

def main(file):
    """
    Main function for compiling the file.
    
    Parameters:
        file (str): The name of the file to compile.
    """
    file_name = file.split(".")
    file_name = file_name[0]
    with open(f"{file_name}.py", "w") as f:
        f.write("")
    for line in content_compile:
        # Komentare herausfiltern
        function, value = get_active_function(line)
        write_function(function, file, value)
   
def check_for_format(requestet, value):
    """
    Checks if the value matches the requested format.
    
    Parameters:
        requestet (str): The requested format.
        value (str): The value to check.
    """
    if requestet == "int":
        try:
            int(value)
        except:
            messagebox.askokcancel(f"Error: The value {value} is not a valid integer.")
   
class app:
    """
    Main application class.
    """
    def __init__(self):
        """
        Initializes the application.
        """
        self.root = tk.CTk()
        self.root.title("Ekips Programming Language Compiler")
        self.root.geometry("410x500")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.iconbitmap("icon.ico")
        self.main_frame()
        self.root.mainloop()  

    def main_frame(self):
        """
        Constructs the main application frame.
        """
        heief = 40
        wighf = 120
        tk.CTkLabel(self.root, text="Ekips Programming Language Compiler", text_color="Blue", font=("Arial", 20)).pack(pady=10)
        tk.CTkButton(self.root, text="select and compile file", command=self.select_file, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        tk.CTkButton(self.root, text="select and debug file", command=self.select_file_deb, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        tk.CTkButton(self.root, text="License", command=self.licence, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        tk.CTkButton(self.root, text="About", command=self.about, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        tk.CTkButton(self.root, text="GitHub", command=self.github, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        tk.CTkButton(self.root, text="Help", command=self.help_web, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        tk.CTkLabel(self.root, text="Maximilian Gründinger\nFirst Lego League Team PaRaMeRoS", text_color="Blue",font=("Arial", 9)).pack(pady=10)
        tk.CTkLabel(self.root, text=f"Version {__version__}", text_color="Blue").pack(pady=10)

    def licence(self):
        messagebox.showinfo("License", f"Ekips System Programming License Agreement\nThis License Agreement (the 'Agreement') is entered into by and between Maximilian Gründinger ('Licensor') and the First Lego League Team known as PaRaMeRoS ('Licensee').\n1. License Grant.\nLicensor hereby grants Licensee a non-exclusive, non-transferable license to use and modify the software program known as Ekips System Programming (the 'Program') solely for educational and non-commercial purposes. This license is granted exclusively to the members of the First Lego League Team identified as PaRaMeRoS.\n2. Restrictions.\nLicensee shall not, and shall not permit others to:\na. Use the Program for any purpose other than educational and non-commercial activities within the First Lego League Team.\nb. Allow non-members of the First Lego League Team to use or access the Program.\nc. Commercialize or distribute the Program for financial gain.\nd. Remove or alter any copyright, trademark, or other proprietary notices contained in the Program.\n3. Security.\nLicensor makes no warranties regarding the security of the Program. Licensee acknowledges and agrees that any use of the Program is at their own risk. Licensor shall not be responsible for any security bugs or issues that may arise in connection with the Program.\n4. Term and Termination.\nThis Agreement shall remain in effect until terminated by either party. Licensor reserves the right to terminate this Agreement immediately if Licensee breaches any of its terms. Upon termination, Licensee shall cease all use of the Program and destroy all copies in their possession.\n5. Disclaimer of Warranty.\nTHE PROGRAM IS PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. LICENSOR DISCLAIMS ALL WARRANTIES, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.\n6. Limitation of Liability.\nIN NO EVENT SHALL LICENSOR BE LIABLE FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM, EVEN IF LICENSOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.\n7. Governing Law.\nThis Agreement shall be governed by and construed in accordance with the laws of Germany, Bavaria, Munic.\n8. Entire Agreement.\nThis Agreement constitutes the entire agreement between the parties and supersedes all prior agreements, whether oral or written, with respect to the Program.\nIN WITNESS WHEREOF, the parties hereto have executed this License Agreement as of the effective date.\nLicensor:\nMaximilian Gründinger\nLicensee:\nPaRaMeRoS\nDate: 1.1.2024")
   
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.app.destroy()
            exit(0)
            
    def select_file(self):
        file = filedialog.askopenfilename(filetypes=[("Ekips System Programming", "*.ssp")])
        if file:
            self.file = file
            compile(file)
            main(file)
            
    def select_file_deb(self):
        file = filedialog.askopenfilename(filetypes=[("Ekips System Programming", "*.ssp")])
        if file:
            self.file = file
            compile(file)
            main_debug(file)
            
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            exit(0)
            
    def credit(self):
        messagebox.showinfo("Credit", "Maximilian Gründinger\nFirst Lego League Team PaRaMeRoS")
        
    def about(self):
        messagebox.showinfo("About", f"Ekips System Programming\nVersion {__version__}\nMaximilian Gründinger\nFirst Lego League Team PaRaMeRoS")
    
    def github(self):
        website.open("https://github.com/Ekips-Prime-Pro/Ekips-Programming-Language")
        
    def help_web(self):
        website.open("https://parameros.net/pro")
     
        
        
if __name__ == "__main__":
    app()