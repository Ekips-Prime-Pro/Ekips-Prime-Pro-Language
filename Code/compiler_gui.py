from __future__ import annotations
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
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from binascii import crc32 as _crc32
from abc import ABC
import struct

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
DELIMITER = 0x02
NO_DELIMITER = 0xFF
COBS_CODE_OFFSET = DELIMITER
MAX_BLOCK_SIZE = 84
XOR = 3
    

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
def encode(data: bytes):
    """
    Encode data using COBS algorithm, such that no delimiters are present.
    """
    buffer = bytearray()
    code_index = block = 0
    def begin_block():
        """Append code word to buffer and update code_index and block"""
        nonlocal code_index, block
        code_index = len(buffer)  # index of incomplete code word
        buffer.append(NO_DELIMITER)  # updated later if delimiter is encountered
        block = 1  # no. of bytes in block (incl. code word)

    begin_block()
    for byte in data:
        if byte > DELIMITER:
            # non-delimeter value, write as-is
            buffer.append(byte)
            block += 1

        if byte <= DELIMITER or block > MAX_BLOCK_SIZE:
            # block completed because size limit reached or delimiter found
            if byte <= DELIMITER:
                # reason for block completion is delimiter
                # update code word to reflect block size
                delimiter_base = byte * MAX_BLOCK_SIZE
                block_offset = block + COBS_CODE_OFFSET
                buffer[code_index] = delimiter_base + block_offset
            # begin new block
            begin_block()

    # update final code word
    buffer[code_index] = block + COBS_CODE_OFFSET

    return buffer


def decode(data: bytes):
    """
    Decode data using COBS algorithm.
    """
    buffer = bytearray()

    def unescape(code: int):
        """Decode code word, returning value and block size"""
        if code == 0xFF:
            # no delimiter in block
            return None, MAX_BLOCK_SIZE + 1
        value, block = divmod(code - COBS_CODE_OFFSET, MAX_BLOCK_SIZE)
        if block == 0:
            # maximum block size ending with delimiter
            block = MAX_BLOCK_SIZE
            value -= 1
        return value, block

    value, block = unescape(data[0])
    for byte in data[1:]:  # first byte already processed
        block -= 1
        if block > 0:
            buffer.append(byte)
            continue

        # block completed
        if value is not None:
            buffer.append(value)

        value, block = unescape(byte)

    return buffer


def pack(data: bytes):
    """
    Encode and frame data for transmission.
    """
    buffer = encode(data)

    # XOR buffer to remove problematic ctrl+C
    for i in range(len(buffer)):
        buffer[i] ^= XOR

    # add delimiter
    buffer.append(DELIMITER)
    return bytes(buffer)


def unpack(frame: bytes):
    """
    Unframe and decode frame.
    """
    start = 0
    if frame[0] == 0x01:  # unused priority byte
        start += 1
    # unframe and XOR
    unframed = bytes(map(lambda x: x ^ XOR, frame[start:-1]))
    return bytes(decode(unframed))

def crc(data: bytes, seed=0, align=4):
    """
    Calculate the CRC32 of data with an optional seed and alignment.
    """
    remainder = len(data) % align
    if remainder:
        data += b"\x00" * (align - remainder)
    return _crc32(data, seed)

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
            if function == "//" or function == "#":
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
            
class BaseMessage(ABC):
    @property
    def ID(cls) -> int:
        raise NotImplementedError

    def serialize(self) -> bytes:
        raise NotImplementedError

    @staticmethod
    def deserialize(data: bytes) -> BaseMessage:
        raise NotImplementedError

    def __str__(self) -> str:
        props = vars(self)
        plist = ", ".join(f"{k}={v}" for k, v in props.items())
        return f"{self.__class__.__name__}({plist})"


def StatusResponse(name: str, id: int):
    class BaseStatusResponse(BaseMessage):
        ID = id

        def __init__(self, success: bool):
            self.success = success

        @staticmethod
        def deserialize(data: bytes):
            id, status = struct.unpack("<BB", data)
            return BaseStatusResponse(status == 0x00)

    BaseStatusResponse.__name__ = name
    return BaseStatusResponse


class InfoRequest(BaseMessage):
    ID = 0x00

    def serialize(self):
        return b"\0"


class InfoResponse(BaseMessage):
    ID = 0x01

    def __init__(
        self,
        rpc_major: int,
        rpc_minor: int,
        rpc_build: int,
        firmware_major: int,
        firmware_minor: int,
        firmware_build: int,
        max_packet_size: int,
        max_message_size: int,
        max_chunk_size: int,
        product_group_device: int,
    ):
        self.rpc_major = rpc_major
        self.rpc_minor = rpc_minor
        self.rpc_build = rpc_build
        self.firmware_major = firmware_major
        self.firmware_minor = firmware_minor
        self.firmware_build = firmware_build
        self.max_packet_size = max_packet_size
        self.max_message_size = max_message_size
        self.max_chunk_size = max_chunk_size
        self.product_group_device = product_group_device

    @staticmethod
    def deserialize(data: bytes) -> InfoResponse:
        (
            id,
            rpc_major,
            rpc_minor,
            rpc_build,
            firmware_major,
            firmware_minor,
            firmware_build,
            max_packet_size,
            max_message_size,
            max_chunk_size,
            product_group_device,
        ) = struct.unpack("<BBBHBBHHHHH", data)
        return InfoResponse(
            rpc_major,
            rpc_minor,
            rpc_build,
            firmware_major,
            firmware_minor,
            firmware_build,
            max_packet_size,
            max_message_size,
            max_chunk_size,
            product_group_device,
        )


class ClearSlotRequest(BaseMessage):
    ID = 0x46

    def __init__(self, slot: int):
        self.slot = slot

    def serialize(self):
        return struct.pack("<BB", self.ID, self.slot)


ClearSlotResponse = StatusResponse("ClearSlotResponse", 0x47)


class StartFileUploadRequest(BaseMessage):
    ID = 0x0C

    def __init__(self, file_name: str, slot: int, crc: int):
        self.file_name = file_name
        self.slot = slot
        self.crc = crc

    def serialize(self):
        encoded_name = self.file_name.encode("utf8")
        if len(encoded_name) > 31:
            raise ValueError(
                f"UTF-8 encoded file name too long: {len(encoded_name)} +1 >= 32"
            )
        fmt = f"<B{len(encoded_name)+1}sBI"
        return struct.pack(fmt, self.ID, encoded_name, self.slot, self.crc)


StartFileUploadResponse = StatusResponse("StartFileUploadResponse", 0x0D)


class TransferChunkRequest(BaseMessage):
    ID = 0x10

    def __init__(self, running_crc: int, chunk: bytes):
        self.running_crc = running_crc
        self.size = len(chunk)
        self.payload = chunk

    def serialize(self):
        fmt = f"<BIH{self.size}s"
        return struct.pack(fmt, self.ID, self.running_crc, self.size, self.payload)


TransferChunkResponse = StatusResponse("TransferChunkResponse", 0x11)


class ProgramFlowRequest(BaseMessage):
    ID = 0x1E

    def __init__(self, stop: bool, slot: int):
        self.stop = stop
        self.slot = slot

    def serialize(self):
        return struct.pack("<BBB", self.ID, self.stop, self.slot)


ProgramFlowResponse = StatusResponse("ProgramFlowResponse", 0x1F)


class ProgramFlowNotification(BaseMessage):
    ID = 0x20

    def __init__(self, stop: bool):
        self.stop = stop

    @staticmethod
    def deserialize(data: bytes) -> ProgramFlowNotification:
        id, stop = struct.unpack("<BB", data)
        return ProgramFlowNotification(bool(stop))


class ConsoleNotification(BaseMessage):
    ID = 0x21

    def __init__(self, text: str):
        self.text = text

    @staticmethod
    def deserialize(data: bytes) -> ConsoleNotification:
        text_bytes = data[1:].rstrip(b"\0")
        return ConsoleNotification(text_bytes.decode("utf8"))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.text!r})"


class DeviceNotificationRequest(BaseMessage):
    ID = 0x28

    def __init__(self, interval_ms: int):
        self.interval_ms = interval_ms

    def serialize(self):
        return struct.pack("<BH", self.ID, self.interval_ms)


DeviceNotificationResponse = StatusResponse("DeviceNotificationResponse", 0x29)

DEVICE_MESSAGE_MAP = {
    0x00: ("Battery", "<BB"),
    0x01: ("IMU", "<BBBhhhhhhhhh"),
    0x02: ("5x5", "<B25B"),
    0x0A: ("Motor", "<BBBhhbi"),
    0x0B: ("Force", "<BBBB"),
    0x0C: ("Color", "<BBbHHH"),
    0x0D: ("Distance", "<BBh"),
    0x0E: ("3x3", "<BB9B"),
}


class DeviceNotification(BaseMessage):
    ID = 0x3C

    def __init__(self, size: int, payload: bytes):
        self.size = size
        self._payload = payload
        self.messages = []
        data = payload[:]
        while data:
            id = data[0]
            if id in DEVICE_MESSAGE_MAP:
                name, fmt = DEVICE_MESSAGE_MAP[id]
                size = struct.calcsize(fmt)
                values = struct.unpack(fmt, data[:size])
                self.messages.append((name, values))
                data = data[size:]
            else:
                print(f"Unknown message: {id}")
                break

    @staticmethod
    def deserialize(data: bytes) -> DeviceNotification:
        id, size = struct.unpack("<BH", data[:3])
        if len(data) != size + 3:
            print(f"Unexpected size: {len(data)} != {size} + 3")
        return DeviceNotification(size, data[3:])

    def __str__(self) -> str:
        updated = list(map(lambda x: x[0], self.messages))
        return f"{self.__class__.__name__}({updated})"


KNOWN_MESSAGES = {
    M.ID: M
    for M in (
        InfoRequest,
        InfoResponse,
        ClearSlotRequest,
        ClearSlotResponse,
        StartFileUploadRequest,
        StartFileUploadResponse,
        TransferChunkRequest,
        TransferChunkResponse,
        ProgramFlowRequest,
        ProgramFlowResponse,
        ProgramFlowNotification,
        ConsoleNotification,
        DeviceNotificationRequest,
        DeviceNotificationResponse,
        DeviceNotification,
    )
}


def deserialize(data: bytes):
    message_type = data[0]
    if message_type in KNOWN_MESSAGES:
        return KNOWN_MESSAGES[message_type].deserialize(data)
    raise ValueError(f"Unknown message: {data.hex(' ')}")



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

            data = unpack(data)
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
        frame = pack(payload)
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
