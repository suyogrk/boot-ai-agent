import argparse
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

from google.genai import types

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
)


def call_function(function_call: types.FunctionCall, verbose=False):
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_name: str = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool",
             parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
             ]
             )

    args_copy = dict(function_call.args) if function_call.args else {}

    args_copy['working_directory'] = "./calculator"

    result = function_map[function_name](**args_copy)

    return types.Content(role="tool", parts=[
        types.Part.from_function_response(name=function_name,response={"result": result})
    ])



    
