from subprocess import CompletedProcess
import subprocess
import os
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the provided python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Path of the current working directory",
            ),
            "file_path": types.Schema(type= types.Type.STRING, description="The path of the python file that is to be run"),
            "args": types.Schema(type = types.Type.OBJECT, description="The arguments provided when the python file is being run")
        },
    ),
)

def run_python_file(working_directory: str, file_path: str, args=None):
    try:
        print(working_directory)
        print(file_path)
        absolute_path = os.path.abspath(working_directory)
        joined_path = os.path.join(absolute_path, file_path)
        normalized_path = os.path.normpath(joined_path)

        is_valid_target_dir = os.path.commonpath([absolute_path, normalized_path]) == absolute_path
        if not is_valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        is_file = os.path.isfile(normalized_path)

        if not is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        does_end_in_py = file_path.endswith('.py')

        if not does_end_in_py:
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", normalized_path]
        
        if args:
            command.extend(args)
        
        result: CompletedProcess = subprocess.run(args=command, cwd=absolute_path, capture_output=True, text=True, timeout=30)

        outstring: str = ""

        if not result.returncode:
            outstring += f"Process exited with code {result.returncode}"

        if not result.stderr or not result.stdout:
            outstring += f"\nNo output produced"

        if result.stderr:
            outstring += f"\nSTDERR: {result.stderr}"
        if result.stdout:
            outstring += f"\nSTDOUT: {result.stdout}"

        return outstring
    except Exception as e:
        return f"Error: executing Python file: {e}"