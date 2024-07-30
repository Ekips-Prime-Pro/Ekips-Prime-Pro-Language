import webbrowser as website
import customtkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import sys
import zipfile
import json
import os
from datetime import datetime
import threading
import asyncio
from typing import cast, TypeVar
import cobs
from messages import *
from crc import crc
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

TMessage = TypeVar("TMessage", bound="BaseMessage")

# Variables
content_compile = []
last_function = "False"
file_name = ""
conf_file = "conf.json"
__version__ = "0.0.0"
llsp3_file_path = 'Projekt.llsp3'
extracted_folder = llsp3_file_path + 'projectbody.json'

SCAN_TIMEOUT = 10.0
SERVICE = "0000fd02-0000-1000-8000-00805f9b34fb"
RX_CHAR = "0000fd02-0001-1000-8000-00805f9b34fb"
TX_CHAR = "0000fd02-0002-1000-8000-00805f9b34fb"
DEVICE_NOTIFICATION_INTERVAL_MS = 5000
EXAMPLE_SLOT = 0
    

with open(conf_file, "r") as file:
    content = json.load(file)
    calibrate = content["calibrate"]
    __version__ = content["version"]
    module = content["module"]
    motor = content["motor"]
    sensor = content["sensor"]
    variables = content["variables"]
    ai = content["ai"]
    switch = content["switch"]

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
    function, variable = content_line.split("(")
    variable = variable.replace("(","")
    variable = variable.replace(")","")
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
    global last_function
    print(f"Writing {function} function...")
    file_name = file.split(".")
    file_name = file_name[0]
    with open(f"{file_name}.py", "a") as f:
        match function:
            case "log":
                if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                    f.write(f"\n  print('{str(value)}')")
                elif last_function == "switch":
                    f.write(f"\n    print('{str(value)}')")
                else:
                    f.write(f"\nprint('{str(value)}')")
            case "sleep":
                sleep_out = f"\ntime.sleep({str(value)})"
                f.write(sleep_out)
            case "init":
                init_out = f"\nimport force_sensor, distance_sensor, motor, motor_pair\nfrom hub import port\nimport time\nfrom app import linegraph as ln\nimport runloop\nfrom math import *\nimport random\nimport math\n"
                f.write(init_out)
            case "ai.init":
                ai_content = ai
                for line in ai_content:
                    f.write(line)
            case "module.init":
                for line in module:
                    f.write(line)
            case "motor.init":
                for line in motor:
                    f.write(line)
            case "sensor.init":
                for line in sensor:
                    f.write(line)
            case "calibration.init":
                for line in calibrate:
                   f.write(line)
            case "variable.init":
                for line in variables:
                    f.write(line)
            case "switch.init":
                for line in switch:
                    f.write("\n")
                    f.write(line)
            case "drive":
                if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                    f.write(f"\n  await drive({value})")
                elif last_function == "switch":
                    f.write(f"\n    await drive({value})")
                else:
                    f.write(f"\n  await drive({value})")
            case "tank":
                if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                    f.write(f"\n  await tank({value})")
                elif last_function == "switch":
                    f.write(f"\n    await tank({value})")
                else:
                    f.write(f"\n  await tank({value})")
            case "obstacle":
                if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                    f.write(f"\n  await obstacle({value})")
                elif last_function == "switch":
                    f.write(f"\n    await obstacle({value})")
                else:
                    f.write(f"\n  await obstacle({value})")
            case "module":
                if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                    f.write(f"\n  await module({value})")
                elif last_function == "switch":
                    f.write(f"\n    await module({value})")
                else:
                    f.write(f"\n  await module({value})")
            case "calibrate":
                if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                    f.write("\n  await calibrate()")
                elif last_function == "switch":
                    f.write("\n    await calibrate()")
                else:
                    f.write("\n  await calibrate()")
            case "main.init":
                f.write("\nasync def main():")
            case "main.run":
                f.write("\nrunloop.run(main())")
            case "switch":
                if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                    f.write("\n  if await switch():")
                elif last_function == "switch":
                    pass
                else:
                    f.write("\n  if await switch():")
            case "call":
                if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                    f.write(f"\n  await {value}()")
                elif last_function == "switch":
                    f.write(f"\n    await {value}()")
            case "generate_ab":
                f.write(f"\nasync def {value}():") # async dev (value) <- function_name()
            case "ai.run":
                if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                    f.write("\n  global calibration")
                    f.write(f"\n  new_data_point = {value}") # {'Kalibrierung': calibration, 'Batterieladestand': 85, 'Reifennutzung': 0.95}
                    f.write("\n  calibration = knn_predict(data, new_data_point, k=3)")
                    f.write("\n  print(f'Vorhergesagte Multiplikation: {calibration}')")
                elif last_function == "switch":
                    f.write("\n    global calibration")
                    f.write(f"\n    new_data_point = {value}") # {'Kalibrierung': calibration, 'Batterieladestand': 85, 'Reifennutzung': 0.95}
                    f.write("\n    calibration = knn_predict(data, new_data_point, k=3)")
                    f.write("\n    print(f'Vorhergesagte Multiplikation: {calibration}')")
            case _:
                if function == "//" or function == "#":
                    f.write(f"\n# {value}")
                else:
                    print(f"Error: The function {function} does not exist.")
                    sys.exit(1)
        last_function = function
        print(f"{last_function} function written...")

def debug_function(function,value=False):
    """
    Debugs the specified function.

    Parameters:
        function (str): The function to debug.
        value (str, optional): The value associated with the function. Defaults to False.
    """
    print(f"Debuging {function} function...")
    global last_function
    match function:
        case "log":
            pass
        case "sleep":
            check_for_format("int", value)
        case "init":
            pass
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
        case "ai.run":
            pass
        case "module":
            check_for_format("int", value)
        case "calibrate":
            pass
        case "main.init":
            pass
        case "main.run":
            pass
        case "switch":
            pass
        case "call":
            pass
        case "generate_ab":
            pass
        case _:
            if function == "//":
                pass
            elif function == "#":
                pass
            else:
                print(f"Error: The function {function} does not exist.")
                messagebox.info("Debugger", f"Error: The function{function} does not exist!")
                sys.exit(1)
    last_function = function
    print(f"Debugging {function} function...")


def compile_llsp3(file, directory, project_name):
    os.makedirs(directory, exist_ok=True)
    projectbody_data = {
        "main": ""
    }
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
    projectbody_path = os.path.join(directory, 'projectbody.json')
    with open(file, 'r') as file:
        projectbody_data['main'] = file.read()
    with open(projectbody_path, 'w') as file:
        json.dump(projectbody_data, file)
    icon_svg_path = os.path.join(directory, 'icon.svg')
    with open(icon_svg_path, 'w') as file:
        file.write(icon_svg_content)
    current_datetime = datetime.utcnow().isoformat() + 'Z'
    manifest_data = {
        "type": "python",
        "appType": "llsp3",
        "autoDelete": False,
        "created": current_datetime,
        "id": "wJI4suuRFvcs",
        "lastsaved": current_datetime,
        "size": 1004,
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
    llsp3_file_path = os.path.join(directory, project_name + '.llsp3')
    with zipfile.ZipFile(llsp3_file_path, 'w') as zip_ref:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, directory)
                zip_ref.write(file_path, arcname)

    if os.path.exists(llsp3_file_path):
        os.remove(manifest_path)
        os.remove(icon_svg_path)
        os.remove(projectbody_path)
        os.rmdir(directory)
        os.remove(os.path.join(directory, project_name + '.py')) # Remove this File if you want to debug the app / if the .llsp3 file is not working

def threaded_debug(function, value=False):
    debug_thread = threading.Thread(target=debug_function, args=(function, value))
    debug_thread.start()
    debug_thread.join()

def main_debug(file):
    """
    Main function for debugging the compiled file.

    Parameters:
        file (str): The name of the file to debug.
    """
    for line in content_compile:
        function, value = get_active_function(line)
        threaded_debug(function, value)

def main(file):
    """
    Main function for compiling the file.

    Parameters:
        file (str): The name of the file to compile.
    """
    file_name = file.split(".")
    file_dir = file_name[1]
    file_name = file_name[0]
    with open(f"{file_name}.py", "w") as f:
        f.write("")
    for line in content_compile:
        function, value = get_active_function(line)
        write_function(function, file, value)
    compile_llsp3(file_name + ".py", file_dir, file_name)

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
            
class connect:
    def main():
        pass


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
        self.stop_event = asyncio.Event()
        self.client = None
        self.info_response = None

    async def scan_and_connect(self):
        def match_service_uuid(device: BLEDevice, adv: AdvertisementData) -> bool:
            return SERVICE.lower() in adv.service_uuids

        print(f"\nScanning for {SCAN_TIMEOUT} seconds, please wait...")
        device = await BleakScanner.find_device_by_filter(
            filterfunc=match_service_uuid, timeout=SCAN_TIMEOUT
        )

        if device is None:
            print("No hubs detected. Ensure that a hub is within range, turned on, and awaiting connection.")
            return False

        device = cast(BLEDevice, device)
        print(f"Hub detected! {device}")

        def on_disconnect(client: BleakClient) -> None:
            print("Connection lost.")
            self.stop_event.set()

        print("Connecting...")
        self.client = BleakClient(device, disconnected_callback=on_disconnect)
        await self.client.connect()
        print("Connected!\n")
        await self.setup_notifications()
        return True

    async def setup_notifications(self):
        service = self.client.services.get_service(SERVICE)
        rx_char = service.get_characteristic(RX_CHAR)
        tx_char = service.get_characteristic(TX_CHAR)

        # simple response tracking
        self.pending_response = (-1, asyncio.Future())

        # callback for when data is received from the hub
        def on_data(_: BleakGATTCharacteristic, data: bytearray) -> None:
            if data[-1] != 0x02:
                # packet is not a complete message
                un_xor = bytes(map(lambda x: x ^ 3, data))  # un-XOR for debugging
                print(f"Received incomplete message:\n {un_xor}")
                return

            data = cobs.unpack(data)
            try:
                message = deserialize(data)
                print(f"Received: {message}")
                if message.ID == self.pending_response[0]:
                    self.pending_response[1].set_result(message)
                if isinstance(message, DeviceNotification):
                    updates = list(message.messages)
                    updates.sort(key=lambda x: x[1])
                    lines = [f" - {x[0]:<10}: {x[1]}" for x in updates]
                    print("\n".join(lines))
            except ValueError as e:
                print(f"Error: {e}")

        await self.client.start_notify(tx_char, on_data)

    async def send_message(self, message: BaseMessage) -> None:
        print(f"Sending: {message}")
        payload = message.serialize()
        frame = cobs.pack(payload)
        packet_size = self.info_response.max_packet_size if self.info_response else len(frame)

        for i in range(0, len(frame), packet_size):
            packet = frame[i : i + packet_size]
            await self.client.write_gatt_char(RX_CHAR, packet, response=False)

    async def send_request(self, message: BaseMessage, response_type: type[TMessage]) -> TMessage:
        self.pending_response = (response_type.ID, asyncio.Future())
        await self.send_message(message)
        return await self.pending_response[1]

    async def execute_program(self, program_data: bytes):
        try:
            self.info_response = await self.send_request(InfoRequest(), InfoResponse)
            notification_response = await self.send_request(
                DeviceNotificationRequest(DEVICE_NOTIFICATION_INTERVAL_MS),
                DeviceNotificationResponse,
            )
            if not notification_response.success:
                print("Error: failed to enable notifications")
                return

            clear_response = await self.send_request(
                ClearSlotRequest(EXAMPLE_SLOT), ClearSlotResponse
            )
            if not clear_response.success:
                print("ClearSlotRequest was not acknowledged. This could mean the slot was already empty, proceeding...")

            program_crc = crc(program_data)
            start_upload_response = await self.send_request(
                StartFileUploadRequest("program.py", EXAMPLE_SLOT, program_crc),
                StartFileUploadResponse,
            )
            if not start_upload_response.success:
                print("Error: start file upload was not acknowledged")
                return

            running_crc = 0
            for i in range(0, len(program_data), self.info_response.max_chunk_size):
                chunk = program_data[i : i + self.info_response.max_chunk_size]
                running_crc = crc(chunk, running_crc)
                chunk_response = await self.send_request(
                    TransferChunkRequest(running_crc, chunk), TransferChunkResponse
                )
                if not chunk_response.success:
                    print(f"Error: failed to transfer chunk {i}")
                    return

            start_program_response = await self.send_request(
                ProgramFlowRequest(stop=False, slot=EXAMPLE_SLOT), ProgramFlowResponse
            )
            if not start_program_response.success:
                print("Error: failed to start program")
                return

            await self.stop_event.wait()

        except KeyboardInterrupt:
            print("Interrupted by user.")
            self.stop_event.set()
        finally:
            if self.client:
                await self.client.disconnect()

    def run(self, program_data: bytes):
        asyncio.run(self.execute_program(program_data))

    def main_frame(self):
        """
        Constructs the main application frame.
        """
        heief = 40
        wighf = 120
        tk.CTkLabel(self.root, text="Ekips Programming Language Compiler", text_color="Blue", font=("Arial", 20)).pack(pady=10)
        tk.CTkButton(self.root, text="select and compile file", command=self.select_file, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        tk.CTkButton(self.root, text="select and debug file", command=self.select_file_deb, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        tk.CTkButton(self.root, text="Upload to spike prime", command=lambda: self.run_upload(), corner_radius=32, width=wighf, height=heief).pack(pady=10)
        tk.CTkButton(self.root, text="About", command=self.about, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        tk.CTkButton(self.root, text="GitHub", command=self.github, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        tk.CTkButton(self.root, text="Help", command=self.help_web, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        tk.CTkLabel(self.root, text="Maximilian Gründinger\nFirst Lego League Team PaRaMeRoS", text_color="Blue",font=("Arial", 9)).pack(pady=10)
        tk.CTkLabel(self.root, text=f"Version {__version__}", text_color="Blue").pack(pady=10)

    def licence(self):
        messagebox.showinfo("License", f"MIT License")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.app.destroy()
            exit(0)

    def select_file(self):
        global file_name
        file = filedialog.askopenfilename(filetypes=[("Ekips System Programming", "*.scsp")])
        file_name = file
        if file:
            self.file = file
            compile(file)
            main(file)
            messagebox.showinfo("Compile", "The file has been successfully compiled.")

    def select_file_deb(self):
        file = filedialog.askopenfilename(filetypes=[("Ekips System Programming", "*.scsp")])
        if file:
            self.file = file
            compile(file)
            main_debug(file)
            messagebox.showinfo("Debug", "The file has been successfully debugged.")

    def run_upload(self):
        file_path = filedialog.askopenfilename(filetypes=[("Spike Prime", "*.llsp3"), ("Python file", "*.py"), ("All Files", "*.*")])
        file_path_be = file_path.split(".")
        print(file_path_be)
        print(file_path)
        if file_path_be[-1] == "llsp3":
            with zipfile.ZipFile(file_path, "r") as file:
                file.extractall("temp")
            with open("temp/projectbody.json", "r") as file:
                content = json.load(file)
                program_data = content["main"]
                print(program_data)
            os.remove("temp/projectbody.json")
            os.remove("temp/icon.svg")
            os.remove("temp/manifest.json")
            os.removedirs("temp")
            threading.Thread(target=self.upload, args=(program_data,)).start()
        elif file_path_be[-1] == "py":
            with open(file_path, 'rb') as file:
                program_data = file.read()
            print(program_data)
            threading.Thread(target=self.upload, args=(program_data,)).start()

    def upload(self, program_data):
        try:
            if asyncio.run(self.scan_and_connect()):
                self.run(program_data)
            else:
                messagebox.showerror("Error", "Failed to connect to hub.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

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
