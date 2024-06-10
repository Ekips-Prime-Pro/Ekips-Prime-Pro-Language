# Imports
import webbrowser as website
import customtkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import sys
import zipfile
import json
import os
from datetime import datetime

# Variables
content_compile = []
file_name = ""
conf_file = "conf.json"
__version__ = "0.0.0.0"
llsp3_file_path = 'Projekt.llsp3'
extracted_folder = llsp3_file_path + 'projectbody.json'

with open(conf_file, "r") as file:
    content = json.load(file)
    calibrate = content("calibrate")
    __version__ = content("version")
    module = content("module")
    motor = content("motor")
    sensor = content("sensor")
    variables = content("variables")
    
    
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

def compile_llsp3(file):
    def calculate_file_size(filepath):
        return os.path.getsize(filepath)

    def create_project(directory, project_id, project_name):
        os.makedirs(directory, exist_ok=True)

        projectbody_data = {
            "main": ""
        }
        projectbody_path = os.path.join(directory, 'projectbody.json')
        with open(projectbody_path, 'w') as file:
            json.dump(projectbody_data, file)

        icon_svg_content = """
        <svg width="60" height="60" xmlns="http://www.w3.org/2000/svg">
            <g fill="none" fill-rule="evenodd">
                <g fill="#D8D8D8" fill-rule="nonzero">
                    <path d="M34.613 7.325H15.79a3.775 3.775 0 00-3.776 3.776v37.575a3.775 3.775 0 003.776 3.776h28.274a3.775 3.775 0 003.776-3.776V20.714a.8.8 0 00-.231-.561L35.183 7.563a.8.8 0 00-.57-.238zm-.334 1.6l11.96 12.118v27.633a2.175 2.175 0 01-2.176 2.176H15.789a2.175 2.175 0 01-2.176-2.176V11.1c0-1.202.973-2.176 2.176-2.176h18.49z"/>
                    <path d="M35.413 8.214v11.7h11.7v1.6h-13.3v-13.3z"/>
                </g>
                <path fill="#0290F5" d="M23.291 27h13.5v2.744h-13.5z"/>
                <path fill="#D8D8D8" d="M38.428 27h4.32v2.744h-4.32zM17 27h2.7v2.7H17zM17 31.86h2.7v2.744H17zM28.151 31.861h11.34v2.7h-11.34zM17 36.72h2.7v2.7H17zM34.665 36.723h8.1v2.7h-8.1z"/>
                <path fill="#0290F5" d="M28.168 36.723h4.86v2.7h-4.86z"/>
            </g>
        </svg>
        """
        icon_svg_path = os.path.join(directory, 'icon.svg')
        with open(icon_svg_path, 'w') as file:
            file.write(icon_svg_content)

        projectbody_size = calculate_file_size(projectbody_path)
        icon_svg_size = calculate_file_size(icon_svg_path)

        total_size = projectbody_size + icon_svg_size

        current_datetime = datetime.utcnow().isoformat() + 'Z'

        manifest_data = {
            "type": "python",
            "appType": "llsp3",
            "autoDelete": False,
            "created": current_datetime,
            "id": project_id,
            "lastsaved": current_datetime,
            "size": total_size, 
            "name": project_name,
            "slotIndex": 0,
            "workspaceX": 120,
            "workspaceY": 120,
            "zoomLevel": 0.5,
            "hardware": {
                "python": {
                    "type": "flipper"
                }
            },
            "state": {
                "canvasDrawerOpen": True
            },
            "extraFiles": []
        }
        manifest_path = os.path.join(directory, 'manifest.json')
        with open(manifest_path, 'w') as file:
            json.dump(manifest_data, file)

        llsp3_file_path = os.path.join(directory, 'Projekt.llsp3')
        with zipfile.ZipFile(llsp3_file_path, 'w') as zip_ref:
            for foldername, subfolders, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, directory)
                    zip_ref.write(file_path, arcname)

        llsp3_file_size = os.path.getsize(llsp3_file_path)
        print(f"Die Größe der erstellten .llsp3-Datei beträgt: {llsp3_file_size} Bytes")

        return llsp3_file_path

    def read_and_modify_projectbody(file_path, new_content):
        with open(file_path, 'r') as file:
            data = json.load(file)
        data['main'] = new_content
        with open(file_path, 'w') as file:
            json.dump(data, file)

        directory = os.path.dirname(file_path)
        projectbody_size = calculate_file_size(file_path)
        icon_svg_size = calculate_file_size(os.path.join(directory, 'icon.svg'))
        total_size = projectbody_size + icon_svg_size
        manifest_path = os.path.join(directory, 'manifest.json')

        with open(manifest_path, 'r') as file:
            manifest_data = json.load(file)

        manifest_data['size'] = total_size
        manifest_data['lastsaved'] = datetime.utcnow().isoformat() + 'Z'

        with open(manifest_path, 'w') as file:
            json.dump(manifest_data, file)

        llsp3_file_path = os.path.join(directory, 'Projekt.llsp3')
        with zipfile.ZipFile(llsp3_file_path, 'w') as zip_ref:
            for foldername, subfolders, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, directory)
                    zip_ref.write(file_path, arcname)

        llsp3_file_size = os.path.getsize(llsp3_file_path)
        print(f"Die Größe der aktualisierten .llsp3-Datei beträgt: {llsp3_file_size} Bytes")


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
        global file_name
        file = filedialog.askopenfilename(filetypes=[("Ekips System Programming", "*.ssp")])
        file_name = file
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
