import os
from config import MAX_CHARACTERS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Read and return the contents of a text file within a permitted working directory. "
        "The file path must resolve inside the working directory. "
        "If the file is too large, the content may be truncated."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["working_directory", "file_path"],
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Absolute or relative base directory that acts as a security boundary. "
                    "The requested file must resolve inside this directory."
                ),
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the file to read, relative to the working directory. "
                    "Must refer to a regular text file."
                ),
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:

        absolute_path = os.path.abspath(working_directory)
        joined_path = os.path.join(absolute_path, file_path)
        normalized_path = os.path.normpath(joined_path)

        is_valid_target_dir = os.path.commonpath([absolute_path, normalized_path]) == absolute_path
        if not is_valid_target_dir:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

        is_file = os.path.isfile(normalized_path)

        if not is_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(normalized_path) as f:
            file_content = f.read(MAX_CHARACTERS)
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'

            return file_content
    except Exception as e:
        return f"Error: {e}"



    