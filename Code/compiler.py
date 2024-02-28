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
    if file.endswith(".scsp"):
        with open(file, "r") as f:
            content = f.readlines()
            for line in content:
                content_compile.append(line)
    else:
        print("Error: File not supported")
        sys.exit(1)

def get_active_function(line):
    content_line = line
    function, variable = content_line.split("(")
    variable = variable.replace("(","")
    variable = variable.replace(")","")
    return function, variable
    
def write_function(function,value): # implement match case
    if function == "print":
        print(f"print('{value}')")
    elif function == "sleep":
        print(f"time.sleep('{value}')")
    else:
        print(f"Compile Error {function} not valid")
        
def main():
    for line in content_compile:
        function, value = get_active_function(line)
        write_function(function, value)
    
    
# main
@click.command()
@click.argument("file", type=click.Path(exists=True), help="File to compile")
@click.version_option("1.0", "--version", "-v", message="Version %(version)s", help="Show version", prog_name="Spike Custom Programming Language Compiler")
def cli(file):
    try:
        if not os.path.isfile(file):
            click.echo(f"Error: The file {file} does not exist.", err=True)
            sys.exit(1)

        compile(file)
        main()
        click.echo(f"Successfully compiled {file}.")

    except Exception as e:
        click.echo(f"Error: An error occurred during compilation. {str(e)}", err=True)