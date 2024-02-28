content_compile = ["print(Hello World", "sleep(6)"]

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
        
for line in content_compile:
    function, value = get_active_function(line)
    write_function(function, value)
    
