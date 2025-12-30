import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Write text content to a file within a permitted working directory. "
        "Parent directories are created automatically if they do not exist. "
        "The target path must resolve inside the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["working_directory", "file_path", "content"],
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Absolute or relative base directory that defines the security boundary. "
                    "The file path must resolve inside this directory."
                ),
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the file to write, relative to the working directory. "
                    "If the file does not exist, it will be created."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Text content to write to the file. "
                    "Binary data must be encoded as text (e.g., base64)."
                ),
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        absolute_path = os.path.abspath(working_directory)
        joined_path = os.path.join(absolute_path, file_path)
        normalized_path = os.path.normpath(joined_path)

        is_valid_target_dir = os.path.commonpath([absolute_path, normalized_path]) == absolute_path
        if not is_valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        is_directory = os.path.isdir(normalized_path)
        if is_directory:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(normalized_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        with open(normalized_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
