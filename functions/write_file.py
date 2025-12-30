import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the contents to the provided file path in the working directory. If the folders do not exist they are created.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base working directory",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file where the content is being written."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The actual content that is written to the file."
            )
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
