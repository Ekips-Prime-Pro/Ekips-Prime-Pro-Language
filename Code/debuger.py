# Imports
import os
import sys
import shutil
import webbrowser as website
import click 
import customtkinter as tk


# Variables
content_compile = []
__version__ = "0.0.0.0"

with open("version", "r") as f:
    __version__ = f.read()

# Functions
def compile(file):
    """
    Compiles the given file if it has a valid extension (.ssp).
    
    Parameters:
        file (str): The path of the file to compile.
    """
    click.echo(f"Compiling {file}...")
    if file.endswith(".ssp"):
        with open(file, "r") as f:
            content = f.readlines()
            for line in content:
                content_compile.append(line)
    else:
        click.echo(f"Error: The file {file} is not a valid file type.", err=True)
        sys.exit(1)

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

def debug_function(function,value=False):
    """
    Debugs the specified function.
    
    Parameters:
        function (str): The function to debug.
        value (str, optional): The value associated with the function. Defaults to False.
    """
    click.echo(f"Debuging {function} function...")
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
                    click.echo(f"Error: The AI {value} does not exist.", err=True)
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
        case "variables.init":
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
                    click.echo(f"Error: The sensor {value} does not exist.", err=True)
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
                click.echo(f"Error: The function {function} does not exist.", err=True)
                exit(1)
            
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
            click.echo(f"Error: The value {value} is not a valid integer.", err=True)
            sys.exit(1)
 
# main
@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.version_option("1.0", "--version", "-v", message=f"Version {__version__}", help="Show version", prog_name="Ekips Programming Language Debuger")
@click.option("--update", "-u", is_flag=True, help="Check for updates.")
@click.option("--syntax", "-s", is_flag=True, help="Show the syntax of the language.")
@click.help_option("--help", "-h", help="Show this help message and exit")
def cli(file, update, syntax):
    """
    Command-line interface for the Ekips Programming Language Debugger.
    
    Parameters:
        file (str): The path of the file to debug.
        update (bool): Flag to check for updates.
        syntax (bool): Flag to show the syntax of the language.
    """
    if syntax:
        website.open("https://github.com/Ekips-Prime-Pro/Ekips-Programming-Language")
    elif update:
        click.echo("Checking for updates...")
    try:
        if not os.path.isfile(file):
            click.echo(f"Error: The file {file} does not exist.", err=True)
            sys.exit(1)

        compile(file)
        main_debug(file)
        click.echo(f"Successfully debug without error {file}.")

    except Exception as e:
        click.echo(f"Error: An error occurred during compilation. {str(e)}", err=True)
        sys.exit(1)
   
if __name__ == "__main__":
    cli()