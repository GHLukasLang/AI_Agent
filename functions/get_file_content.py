import os

def get_file_content(working_directory, file_path):
    
    #get the absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)

    #check if file_path is within the working directory
    if abs_working_dir != abs_path and not abs_path.startswith(abs_working_dir + "/"):
        error_file_outside =  f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        return error_file_outside

    #check if file_path is a file
    if os.path.isfile(abs_path) is False:
        error_no_file = f'Error: File not found or is not a regular file: "{file_path}"'
        return error_no_file

    MAX_CHARS = 10000

    with open(abs_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        extra = f.read(1)
        truncated_note = f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string + truncated_note if extra != "" else file_content_string

        
        
