import os
import subprocess

def run_python_file(working_directory, file_path):
    #get the absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)

    #check if file_path is within the working directory
    if abs_working_dir != abs_path and not abs_path.startswith(abs_working_dir + "/"):
        error_file_outside =  f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        return error_file_outside

    #check if its a file
    if os.path.isfile(abs_path) is False:
        return f'Error: File "{file_path}" not found.'
    
    #check if its a .py file
    if not abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    file_name = os.path.basename(abs_path)
    
    try:
        result = subprocess.run(["python3", f"{file_name}"], cwd=os.path.dirname(abs_path), capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            exit_message = f"Process exited with code {result.returncode}"
        else:
            exit_message = ""
        if result.stdout == "" and result.stderr == "":
            return "No output produced."
        
        output = [
            f"STDOUT:{result.stdout}",
            f"STDERR:{result.stderr}"
        ]
        if exit_message:
            output.append(exit_message)
        return "\n\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
