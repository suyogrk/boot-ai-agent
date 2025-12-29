import os

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
