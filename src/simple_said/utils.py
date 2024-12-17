import json
import sys
import os
import shutil
import datetime

from kutils import determine_keri_version, dict_to_keri_byte_str, dict_to_said_str


def load_json_from_file(file_path):
    """
    Loads a JSON file from the given file path and returns its contents as a dictionary.

    Parameters:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a dictionary.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data



def parse_input_args():
    """
    Custom argument parser for input files and their associated labels and versions.

    Returns:
        list: A list of dictionaries, each containing file information:
              - file_name (str): The input file name.
              - label (str or None): The associated label, if provided.
              - version (str or None): The associated version, if provided.
    """
    args = sys.argv[1:]  # Skip the script name
    file_list = []
    current_file = None
    current_label = None
    current_version = None

    i = 0
    while i < len(args):
        if args[i] in ["-i", "--input"]:  # New input file
            # Save the previous file's data if available
            if current_file:
                file_list.append({
                    "file_name": current_file,
                    "label": current_label,
                    "version": current_version,
                })
            # Start new input file tracking
            current_file = args[i + 1] if i + 1 < len(args) else None
            current_label = None
            current_version = None
            i += 1  # Skip to the next argument
        elif args[i] in ["-d", "--label"]:  # Label for the current input file
            current_label = args[i + 1] if i + 1 < len(args) else None
            i += 1  # Skip to the next argument
        elif args[i] in ["-v", "--version"]:  # Version for the current input file
            current_version = args[i + 1] if i + 1 < len(args) else None
            i += 1  # Skip to the next argument
        i += 1

    # Save the last file's data if available
    if current_file:
        file_list.append({
            "file_name": current_file,
            "label": current_label,
            "version": current_version,
        })
    data_list = []

    for idx in range(len(file_list)):
        try:
            f = os.path.basename(file_list[idx]['file_name'])
            
            with open(file_list[idx]['file_name'], "r") as file:
                json_data = json.load(file)
                print(97, json_data.get("v"))
                label = file_list[idx]['label']
                version = file_list[idx]['version']
                

                # Infer label if not explicitly provided
                if label is None:
                    if "d" in json_data:
                        label = "d"
                    elif "$id" in json_data:
                        label = "$id"

                # Infer version if not explicitly provided
                if version is None:
                    version = json_data.get("v")
                    if version is not None:
                        version= determine_keri_version(dict_to_keri_byte_str(json_data))

                data_list.append(
                    {
                        "file_path": f,
                        "file_name": os.path.basename(f),
                        "label": label,
                        "version": version,
                        "data": json_data,
                    }
                )
        except FileNotFoundError:
            print(f"Error: The file '{f}' was not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: The file '{f}' is not valid JSON.")
            sys.exit(1)

    return data_list


def get_file_length_in_chars(file_path):
        """
        Reads a file as a string and returns its character length.
    
        Parameters:
            file_path (str): The path to the file.
    
        Returns:
            int: The length of the file in characters.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            return len(file_content)

def create_backup_directory(existing_dir):
    """
    Creates a new directory in the same location as `existing_dir` with a timestamp.

    Parameters:
        existing_dir (str): The path of the existing directory.

    Returns:
        str: The path of the new backup directory.
    """
    # Get the current timestamp in the required format
    timestamp = datetime.datetime.now().strftime("%m%d%Y_%H%M%S")
    
    # Construct the new directory name
    new_dir_name = f"{os.path.basename(existing_dir)}_bu_{timestamp}"
    
    # Get the parent directory path
    parent_dir = os.path.dirname(existing_dir)
    
    # Full path for the new directory
    new_dir_path = os.path.join(parent_dir, new_dir_name)
    
    # Create the new directory
    os.makedirs(new_dir_path, exist_ok=True)
    
    print(f"Created new directory: {new_dir_path}")
    return new_dir_path



def copy_file(file_path, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    if os.path.isfile(file_path):
        shutil.copy(file_path, dest_dir)

def remove_json_whitespace(file_path, out_file=None):
    if out_file == None:
        out_file = file_path
    
    data = load_json_from_file(file_path)

    d = dict_to_said_str(data)

    with open(out_file, 'w') as f:
        f.write(d)

def center_text(text, n, pad_char=' '):
    """
    Centers text within a given number of spots (n).
    If the text is longer than n, it truncates the text.

    Parameters:
        text (str): The text to be centered.
        n (int): The total number of spots.

    Returns:
        str: The centered or truncated text.
    """
    # Truncate text if it's longer than n
    if len(text) > n:
        return text[:n]
    
    # Center text by adding padding on both sides
    left_padding = (n - len(text)) // 2
    right_padding = n - len(text) - left_padding
    return pad_char * left_padding + text + pad_char * right_padding

def get_file_length_in_bytes(file_path):
    """
    Reads a file in as bytes and returns its length.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        int: The length of the file in bytes.
    """
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
        return len(file_bytes)
def read_file_as_bytes(file_path):
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
        return file_bytes

