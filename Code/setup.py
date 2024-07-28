from distutils.core import setup
import py2exe

setup(
    name='Ekips Prime Pro Language Executable',
    version='2.1.2',
    console=[{
        'script': 'compiler_gui.py',
        'icon_resources': [(1, 'icon.ico')],
    }],
    options={
        'py2exe': {
            'bundle_files': 1,  # Bundle everything into a single file
            'compressed': True,  # Compress the library archive
            'optimize': 2,  # Optimize the bytecode
        }
    },
    zipfile=None,  # Do not create a separate library zip file
    data_files=[
        ('images', ['icon.ico', 'image-4.png', 'image-5.png', 'image-6.png']),
        ('config', ['conf.json']),
        ('Others', ['../README.md', '../LICENSE']),
    ]
)