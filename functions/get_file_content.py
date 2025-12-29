import os
from config import MAX_CHARACTERS

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



    