import os

def write_file(working_directory, file_path, content):
    #get the absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    #print("absolute path for working directory:" + abs_working_dir)
    full_path = os.path.join(working_directory, file_path)
    #print("full path for file_path:" + full_path)
    abs_path = os.path.abspath(full_path)
    #print("abs path for the file_path:" + abs_path)

    #check if file_path is within the working directory
    if abs_working_dir != abs_path and not abs_path.startswith(abs_working_dir + "/"):
        error_file_outside =  f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        return error_file_outside
    
   # if os.path.isfile(abs_path) is False:
   #     return f'Error: File "{file_path}" not found.'
    
    #if not abs_path.endswith(".py"):
    #    return f'Error: "{file_path}" is not a Python file.'

    #ensure directory structure exists:
    try:
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    #open for writing:
        with open(abs_path, "w") as f:
        #write
            f.write(content)
            
    except Exception as e:
        return f"Error: An unexpected error occured: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    