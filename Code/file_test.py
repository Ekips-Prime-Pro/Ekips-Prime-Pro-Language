import tkinter as tk
import zipfile
import json
import os

llsp3_manifest = {
    "type": "python",
    "appType": "llsp3",
    "autoDelete": false,
    "created": "2024-05-31T20:11:04.017Z",
    "id": "3hf83l3sq3KS",
    "lastsaved": "2024-05-31T20:28:39.417Z",
    "size": 1039,
    "name": "Projekt 2",
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
        "canvasDrawerOpen": true
    },
    "extraFiles": []
}
llsp3_projectbody = {
    "main": "# This will be stupid \nprint(\"Welcome to the fucking univers\")"
}
llsp3_icon = '<svg width="60" height="60" xmlns="http://www.w3.org/2000/svg">\n    <g fill="none" fill-rule="evenodd">\n        <g fill="#D8D8D8" fill-rule="nonzero">\n            <path d="M34.613 7.325H15.79a3.775 3.775 0 00-3.776 3.776v37.575a3.775 3.775 0 003.776 3.776h28.274a3.775 3.775 0 003.776-3.776V20.714a.8.8 0 00-.231-.561L35.183 7.563a.8.8 0 00-.57-.238zm-.334 1.6l11.96 12.118v27.633a2.175 2.175 0 01-2.176 2.176H15.789a2.175 2.175 0 01-2.176-2.176V11.1c0-1.202.973-2.176 2.176-2.176h18.49z"/>\n            <path d="M35.413 8.214v11.7h11.7v1.6h-13.3v-13.3z"/>\n        </g>\n        <path fill="#0290F5" d="M23.291 27h13.5v2.744h-13.5z"/>\n        <path fill="#D8D8D8" d="M38.428 27h4.32v2.744h-4.32zM17 27h2.7v2.7H17zM17 31.86h2.7v2.744H17zM28.151 31.861h11.34v2.7h-11.34zM17 36.72h2.7v2.7H17zM34.665 36.723h8.1v2.7h-8.1z"/>\n        <path fill="#0290F5" d="M28.168 36.723h4.86v2.7h-4.86z"/>\n    </g>\n</svg>'


# Pfad zur .llsp3-Datei
llsp3_file_path = 'Projekt2.llsp3'
extracted_folder = llsp3_file_path + 'projectbody.json'

# Schritt 1: Entpacken der .llsp3-Datei
with zipfile.ZipFile(llsp3_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)

# Schritt 2: Lesen und Ändern der projectbody.json
projectbody_json_path = os.path.join(extracted_folder, 'projectbody.json')

# Lesen der projectbody.json-Datei
with open(projectbody_json_path, 'r') as file:
    projectbody_data = json.load(file)

# Ausgabe des aktuellen Inhalts von projectbody.json
print("Aktueller Inhalt von projectbody.json:")
print(json.dumps(projectbody_data, indent=4))

# Ändern des Inhalts
projectbody_data['main'] = projectbody_data['main'].replace("Welcome to the fucking univers", "Welcome to the universe")

# Speichern der geänderten projectbody.json-Datei
with open(projectbody_json_path, 'w') as file:
    json.dump(projectbody_data, file, indent=4)

# Schritt 3: Zurückpacken in das .llsp3-Format
new_llsp3_file_path = 'Projekt_neu.llsp3'

# Erstellen einer neuen .llsp3-Datei (ZIP-Format)
with zipfile.ZipFile(new_llsp3_file_path, 'w') as zip_ref:
    for foldername, subfolders, filenames in os.walk(extracted_folder):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            arcname = os.path.relpath(file_path, extracted_folder)
            zip_ref.write(file_path, arcname)

print(f'Die geänderte .llsp3-Datei wurde unter {new_llsp3_file_path} gespeichert.')
