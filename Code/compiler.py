# Imports
import os
import sys
import shutil
import webbrowser as website
import click


# Variables
content_compile = []


# Functions
def compile(file):
    click.echo(f"Compiling {file}...")
    if file.endswith(".scsp"):
        with open(file, "r") as f:
            content = f.readlines()
            for line in content:
                content_compile.append(line)
    else:
        click.echo(f"Error: The file {file} is not a valid file type.", err=True)
        sys.exit(1)

def get_active_function(line):
    content_line = line
    function, variable = content_line.split("(")
    variable = variable.replace("(","")
    variable = variable.replace(")","")
    return function, variable
    
def write_function(function,value,file):
    click.echo(f"Writing {function} function...")
    file_name = file.split(".")
    file_name = file_name[0]
    with open(f"{file_name}.py", "w") as f:
        match function:
            case "print":
                f.write(f"print('{value}')")
            case "sleep":
                f.write(f"time.sleep('{value}')")
        
def main():
    for line in content_compile:
        function, value = get_active_function(line)
        write_function(function, value, file)
    
    
# main
@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.version_option("1.0", "--version", "-v", message="Version 0.1", help="Show version", prog_name="Spike Custom Programming Language Compiler")
@click.help_option("--help", "-h", help="Show this help message and exit")
def cli(file):
    try:
        if not os.path.isfile(file):
            click.echo(f"Error: The file {file} does not exist.", err=True)
            sys.exit(1)

        compile(file)
        main(file)
        click.echo(f"Successfully compiled {file}.")

    except Exception as e:
        click.echo(f"Error: An error occurred during compilation. {str(e)}", err=True)
        sys.exit(1)
