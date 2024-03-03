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

def write_function(function,file,value=False):
    click.echo(f"Writing {function} function...")
    file_name = file.split(".")
    file_name = file_name[0]
    with open(f"{file_name}.py", "a") as f:
        match function:
            case "log":
                print_out = f"print('{str(value)}')\n"
                f.write(print_out)
            case "sleep":
                sleep_out = f"time.sleep({str(value)})\n"
                f.write(sleep_out)
            case "init":
                init_out = f"import force_sensor, distance_sensor, motor, motor_pair\nfrom hub import port\nimport time\nfrom app import linegraph as ln\nimport runloop\nfrom math import *\nimport random\n"
                f.write(init_out)
            case "ai.chose":
                ai_chose_out = f"ai_chose = '{str(value)}'\n"
                f.write(ai_chose_out)
            case "ai.init":
                ai_init_out = f"ai = runloop.AI()\n"
                f.write(ai_init_out)
                with open("ai.fll", "r") as r:
                    ai_content = r.readlines()
                    for line in ai_content:
                        f.write(line)
            case "module.init":
                with open("module.fll", "r") as r:
                    ai_content = r.readlines()
                    for line in ai_content:
                        f.write(line)
            case "motor.init":
                with open("motor.fll", "r") as r:
                    ai_content = r.readlines()
                    for line in ai_content:
                        f.write(line)
            case "sensor.init":
                with open("sensor.fll", "r") as r:
                    ai_content = r.readlines()
                    for line in ai_content:
                        f.write(line)
            case "calibration.init":
                with open("calibration.fll", "r") as r:
                    ai_content = r.readlines()
                    for line in ai_content:
                        f.write(line)
            case "variables.init":
                with open("variables.fll", "r") as r:
                    ai_content = r.readlines()
                    for line in ai_content:
                        f.write(line)
            case "drive":
                f.write(f"  await drive({value})\n")
            case "tank":
                f.write(f"  await tank({value})\n")
            case "obstacle":
                f.write(f"  await obstacle({value})\n")
            case "ai.sensor":
                # add the sensor to the ai input
                f.write(f"ai_sensor.append('{value}\n')")
            case "module":
                f.write(f"  await module({value})\n")
            case "calibrate":
                f.write("   await calibrate()\n")
            case "ai.data_save":
                f.write(f"  write_ai_data('{value}')\n")
            case "ai.data_load":
                for line in value:
                    f.write(f"ai_data.append({line})\n")
            case "main.init":
                f.write("runloop.run(main())\n")
                f.write("async def main():\n")
        
def main(file):
    file_name = file.split(".")
    file_name = file_name[0]
    with open(f"{file_name}.py", "w") as f:
        f.write("")
    for line in content_compile:
        # Komentare herausfiltern
        function, value = get_active_function(line)
        write_function(function, file, value)
    
    
# main
@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.version_option("1.0", "--version", "-v", message="Version 0.1", help="Show version", prog_name="Spike Custom Programming Language Compiler")
@click.option("--format", "-f", type=click.Choice([".py", ".c"]), help="The format to compile to. Default is llsp3.")
@click.option("--update", "-u", is_flag=True, help="Check for updates.")
@click.option("--syntax", "-s", is_flag=True, help="Show the syntax of the language.")
@click.help_option("--help", "-h", help="Show this help message and exit")
def cli(file, format, update, syntax):
    if syntax:
        website.open("https://github.com/Spike-Prime-Pro/Spike-Custom-Programming-Language-and-Compiler/blob/main/README.md")
    elif update:
        click.echo("Checking for updates...")
    elif format:
        click.echo("Compiling to .py...")
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
   
if __name__ == "__main__":
    cli()