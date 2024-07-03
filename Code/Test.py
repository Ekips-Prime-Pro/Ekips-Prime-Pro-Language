import os

def compile_llsp3(file, directory, project_name):
    def calculate_file_size(file_path):
        return os.path.getsize(file_path)
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
    projectbody_size = calculate_file_size(projectbody_path)
    icon_svg_size = calculate_file_size(icon_svg_path)
    total_size = projectbody_size + icon_svg_size
    current_datetime = datetime.utcnow().isoformat() + 'Z'
    manifest_data = {
        "type": "python",
        "appType": "llsp3",
        "autoDelete": False,
        "created": current_datetime,
        "id": "wJI4suuRFvcs",
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
    llsp3_file_path = os.path.join(directory, project_name + '.llsp3')
    with zipfile.ZipFile(llsp3_file_path, 'w') as zip_ref:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, directory)
                zip_ref.write(file_path, arcname)
    llsp3_file_size = os.path.getsize(llsp3_file_path)