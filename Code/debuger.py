# Imports
import os
import sys
import shutil
import webbrowser as website
import click
import customtkinter as tk


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
    function, variable = content_line.split("{")
    variable = variable.replace("{","")
    variable = variable.replace("}","")
    variable = variable.replace("\n","")
    return function, variable

def debug_function(function,value=False):
    click.echo(f"Debuging {function} function...")
    match function:
        case "log":
            pass
        case "sleep":
            pass
        case "init":
            pass
        case "ai.chose":
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
            pass
        case "tank":
            pass
        case "obstacle":
            pass
        case "ai.sensor":
            pass
        case "module":
            pass
        case "calibrate":
            pass
        case "ai.data_save":
            pass
        case "ai.data_load":
            pass
        case "main.init":
            pass
        case _:
            click.echo(f"Error: The function {function} does not exist.", err=True)
            exit(1)
            
def main_debug(file):
    for line in content_compile:
        # Komentare herausfiltern
        function, value = get_active_function(line)
        debug_function(function, value)
        
# main
@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.version_option("1.0", "--version", "-v", message="Version 0.1", help="Show version", prog_name="Spike Custom Programming Language Debuger")
@click.option("--update", "-u", is_flag=True, help="Check for updates.")
@click.option("--syntax", "-s", is_flag=True, help="Show the syntax of the language.")
@click.help_option("--help", "-h", help="Show this help message and exit")
def cli(file, update, syntax):
    if syntax:
        website.open("https://github.com/Spike-Prime-Pro/Spike-Custom-Programming-Language-and-Compiler/blob/main/README.md")
    elif update:
        click.echo("Checking for updates...")
    try:
        if not os.path.isfile(file):
            click.echo(f"Error: The file {file} does not exist.", err=True)
            sys.exit(1)

        compile(file)
        main_debug(file)
        click.echo(f"Successfully compiled {file}.")

    except Exception as e:
        click.echo(f"Error: An error occurred during compilation. {str(e)}", err=True)
        sys.exit(1)
   
if __name__ == "__main__":
    cli()