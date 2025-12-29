import os

def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(working_directory)
        joined_path = os.path.join(absolute_path, directory)
        normalized_path = os.path.normpath(joined_path)

        is_valid_target_dir = os.path.commonpath([absolute_path, normalized_path]) == absolute_path
        if not is_valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(normalized_path):
            return f'Error: "{directory}" is not a directory'
        
        content_list = os.listdir(normalized_path)

        for item in content_list:
            item_size = os.path.getsize(os.path.join(normalized_path, item))
            item_is_dir = os.path.isdir(os.path.join(normalized_path, item))
            print(f"- {item}: file_size={item_size} bytes, is_dir={item_is_dir}")
    except Exception as e:
        return f"Error: {e}"