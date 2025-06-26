import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

from functions.call_function import call_function

###get the key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

#make a client
client = genai.Client(api_key=api_key)

##get the prompt or exit when there is no prompt
try:
    user_prompt = sys.argv[1]
except IndexError:
    print("Error, no prompt given")
    exit(1)

#initialize verbose and check whether on or off
verbose = False
if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    verbose = True


##function declaration get_files_info
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

##function declaration get_file_content
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of the specified file, truncated at 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Filepath of the file to get the content from, relative to the working directory."
            ),
        },
    ),
)

##function declaration write_file
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Let's you write to a file. Overwrites if it does exist, otherwise it will be created.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Filepath of the file to be overwritten or created, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents of the file to be created or overwritten with."
            ),
        },
    ),
)

##function declaration run_python_file
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file. Returns the STDOUT and STDERR.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Filepath of the python file to be run."
            ),
        },
    ),
)

#list which functions are available, to be given in the request
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

##system prompt:
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Get file content
- Write files
- Run Pyhton files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messages = []
iterations = 0
#make the inital message
message = types.Content(role="user", parts=[types.Part(text=user_prompt)])
#and append it to the list, to which the thread will be added during the loop below
messages.append(message)

#FEEDBACK LOOP

while iterations < 20:

    ##get the response
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt),
    )

    if response.function_calls: 
               
        #add the first candidate to the messages list
        if response.candidates and response.candidates[0].content:
            messages.append(response.candidates[0].content)
        #if functions have been called, add their result to the new message
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=verbose)
            try:
                function_call_result.parts[0].function_response.response
            except (AttributeError, IndexError):
                raise Exception("Returned object from call_function did not have the expected structure.")
            
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            messages.append(function_call_result)
    else:
        print(response.text)
        break

    iterations += 1


#if verbose, print more userprompt, prompt tokens and response tokens
if verbose == True:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
