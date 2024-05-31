

# Pfad zur .llsp3-Datei
llsp3_file_path = 'Projekt.llsp3'
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
