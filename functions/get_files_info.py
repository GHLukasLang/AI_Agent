import os

def get_files_info(working_directory, directory=None):
    #if default, assign directory to the working directory
    if directory is None:
        directory = working_directory

    #get the absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    full_directory_path = os.path.join(working_directory, directory)
    abs_dir = os.path.abspath(full_directory_path)


    if abs_working_dir != abs_dir and not abs_dir.startswith(abs_working_dir + "/"):
        error_dir_outside =  f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return error_dir_outside

    #check if directory is a directory  
    if os.path.isdir(abs_dir) is False:
        error_nondir = f'Error: "{directory}" is not a directory'
        return error_nondir
    
    #return a string representing the contents of the directory
    
    try:
        dir_list = sorted(os.listdir(abs_dir))
    except OSError:
        return f"Error: Can't read the directory {directory}"
    
    output_str = ""
    for item in dir_list:
        item_path = os.path.join(abs_dir, item)
        try:
            size = os.path.getsize(item_path)
        except OSError:
            return f"Error: cant get size for {item_path}"
        try:
            is_dir = os.path.isdir(item_path)
        except OSError:
            return f"Error: cant access directory {directory}"
        output_str += f"- {item}: file_size={size} bytes, is_dir={is_dir}\n"
    return output_str
        