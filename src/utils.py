import json
import blake3
import base64

import datetime
import sys
import os
import re
import shutil
import pprint
pp = pprint.PrettyPrinter(indent=2, sort_dicts=False)
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

import sys
import os
import json
import argparse


import sys
import os
import json
import argparse


def load_json_from_cli():
    """
    Reads JSON file paths, labels, and versions from command-line arguments and loads each file.

    Returns:
        list: A list of dictionaries where each entry contains metadata and the content of a JSON file.

    Raises:
        SystemExit: If the required arguments are missing or if there are errors loading any JSON file.
    """
    parser = argparse.ArgumentParser(description="Load JSON files and associate them with labels and versions.")
    parser.add_argument(
        "-i", "--input", action="append", required=True,
        help="Specify input JSON file paths. Use -i multiple times for multiple files."
    )
    parser.add_argument(
        "--label", "-d", "-l", nargs="*", action="append",
        help="Optional labels corresponding to the input files. If not provided, inferred or set to None."
    )
    parser.add_argument(
        "--version", "-v", nargs="*", action="append",
        help="Optional versions corresponding to the input files. If not provided, inferred or set to None."
    )

    args = parser.parse_args()

    # Flatten input files
    # print('args.input ' , args.input )

    # input_files = [file for sublist in args.input for file in sublist]
    input_files = args.input
    # print(input_files)

    # Handle mismatched input counts
    if args.label and len(args.label) > len(input_files):
        print("Error: More labels than input files provided.")
        sys.exit(1)
    if args.version and len(args.version) > len(input_files):
        print("Error: More versions than input files provided.")
        sys.exit(1)

    # Extend missing labels and versions with None
    labels = (args.label or []) + [None] * (len(input_files) - len(args.label or []))
    versions = (args.version or []) + [None] * (len(input_files) - len(args.version or []))
    print('versions',  versions)

    data_list = []

    for idx, file_path in enumerate(input_files):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        label = labels[idx]
        version = versions[idx]
        print('file_name', file_name)
        print(file_path)
        try:
            with open(file_path, "r") as file:
                json_data = json.load(file)

                # Infer label if not provided
                if label is None:
                    if "d" in json_data:
                        label = "d"
                    elif "$id" in json_data:
                        label = "$id"
                    else:
                        label = None  # Set explicitly to None if not inferable

                # Infer version if not provided
                if version is None:
                    if "v" in json_data:
                        version = determine_keri_version(dict_to_said_str(json_data))
                        # version = json_data["version"]
                    else:
                        version = None  # Set explicitly to None if not inferable

                data_list.append(
                    {
                        "file_path": file_path,
                        "file_name": file_name,
                        "label": label,
                        "version": version,
                        "data": json_data,
                    }
                )
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: The file '{file_path}' is not valid JSON.")
            sys.exit(1)

    return data_list


if __name__ == "__main__":
    loaded_data = load_json_from_cli()
    print("Loaded Data:")
    for entry in loaded_data:
        print(entry)


# def load_json_from_cli():
#     """
#     Reads JSON file paths and labels from command-line arguments and loads each file.

#     Returns:
#         dict: A dictionary where each label maps to the contents of the corresponding JSON file.

#     Raises:
#         SystemExit: If the required arguments are missing or if there are errors loading any JSON file.
#     """
#     parser = argparse.ArgumentParser(description="Load JSON files and associate them with labels.")
#     parser.add_argument(
#         "-i",
#         "--input",
#         nargs="+",
#         action='append',
#         required=True,
#         help="List of input JSON file paths. Provide space-separated file paths.",
#     )
#     parser.add_argument(
#         "--label", "-d", "-l", nargs="+", help="Optional labels corresponding to the input files.",
#         action='append'
#     )
#     parser.add_argument("--version", "-v",  nargs="+" , action='append',
#                         # action="store_true", 
#                         help="Display version information.")

#     args = parser.parse_args()
#     input_files = [file for sublist in args.input for file in sublist]

#     # Show version and exit if requested
#     # if args.version:
#     #     print("Version 1.0.0")
#     #     sys.exit(0)

#     if not args.input:
#         print("Error: No input files provided.")
#         sys.exit(1)

#     if args.label and len(args.label) != len(args.input):
#         print("Error: Number of labels must match the number of input files.")
#         sys.exit(1)

#     data_list = []

#     for idx, file_path in enumerate(input_files):
#         print('idx', idx)
#         file_name = os.path.splitext(os.path.basename(file_path))[0]
#         label = args.label[idx] if args.label else None
#         version = args.label[idx] if args.label else None

#         try:
#             with open(file_path, "r") as file:
#                 json_data = json.load(file)
                
#                 # If no label is provided, infer it from the file's data
#                 if not label:
#                     if "d" in json_data:
#                         label = "d"
#                     elif "$id" in json_data:
#                         label = "$id"
#                     else:
#                         print(f"Error: Unable to infer label for file '{file_path}'.")
#                         sys.exit(1)
#                 if version is None:
#                     version = determine_keri_version(dict_to_said_str(json_data))
#                 data_list.append(
#                     {
#                         "file_path": file_path,
#                         "file_name": file_name,
#                         "label": label,
#                         "data": json_data,
#                         'version': version
#                     }
#                 )
#         except FileNotFoundError:
#             print(f"Error: The file '{file_path}' was not found.")
#             sys.exit(1)
#         except json.JSONDecodeError:
#             print(f"Error: The file '{file_path}' is not valid JSON.")
#             sys.exit(1)

#     return data_list


# if __name__ == "__main__":
#     loaded_data = load_json_from_cli()
#     print("Loaded Data:")
#     for entry in loaded_data:
#         print(entry)


# def load_json_from_cli():
#     """
#     Reads JSON file paths and labels from command-line arguments and loads each file.

#     Returns:
#         dict: A dictionary where each label maps to the contents of the corresponding JSON file.

#     Raises:
#         SystemExit: If the required arguments are missing or if there are errors loading any JSON file.
#     """
#     # Ensure there’s an even number of arguments (each file has a path and a label)
#     if (len(sys.argv) - 1) % 2 != 0:
#         print("Usage: python main.py <path1> <label1> <path2> <label2> ...")
#         sys.exit(1)

#     _data = []

#     # Iterate over arguments in pairs (path and label)

#     for i in range(1, len(sys.argv), 2):
#         data = {}
#         file_path = sys.argv[i]
#         file_name = os.path.splitext(os.path.basename(file_path))[0]
#         # print(i)
#         # print(file_path)
#         label = sys.argv[i + 1]
#         # print(label)
#         # Load JSON data for the given file path
#         try:
#             with open(file_path, 'r') as file:
#                 o = {'file_path': file_path,
#                      'file_name': file_name,
#                      'label': label,
#                      'data': {}}
#                 d = json.load(file)

#                 o['data'] = d
#                 _data.append(o)
#         except FileNotFoundError:
#             print(f"Error: The file '{file_path}' was not found.")
#             sys.exit(1)
#         except json.JSONDecodeError:
#             print(f"Error: The file '{file_path}' is not valid JSON.")
#             sys.exit(1)

#     return _data

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

def blake3_to_byte_array(data):
    '''
    compute the BLAKE3 hash and get the bytes (which is a byte array)
    '''
    hasher = blake3.blake3()
    hasher.update(data)
    byte_array = hasher.digest()
    return byte_array

  
def dict_to_said_str(data_dict):
    """
    Convert the dictionary to a JSON string 
    without extra spaces after commas and colons
    """
    json_str = json.dumps(data_dict, separators=(',', ':'))
    return json_str
  
def dict_to_keri_byte_str(data_dict, to_bytes=True):
    # Convert the dictionary to a JSON string without extra spaces after commas and colons
    json_str = json.dumps(data_dict, separators=(',', ':'))
    if to_bytes:
        json_str = json_str.encode('utf-8')
    return json_str

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

def is_bytes(obj):
    return isinstance(obj, bytes)
def is_string(obj):
    return isinstance(obj, str)

def byte_to_bits(byte):
    return format(byte, '08b')
  
def bytes_to_bits(byte_array):
    return ''.join(format(byte, '08b') for byte in byte_array)

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
    
  
def blake3_256_from_dict(dictionary, print_dict=False):
    '''
    get blake3_256 byte array from dictionary
    
    Parameters:
     dictionary(str): a keri compliant string 
     
    Returns: 
     -> encoded bytes -> blake3  -> byte array
    
    '''
    if print_dict:
        print(dict_to_said_str(dictionary).encode('utf-8'))
    return blake3_to_byte_array(dict_to_said_str(dictionary).encode('utf-8'))


def nearest_higher_multiple(x, n):
    """
     Calculate the nearest higher multiple of n greater than or equal to x
    """
    if x % n == 0:
        return x
    else:
        return ((x // n) + 1) * n

B64_VALUES = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

def value_of(ch):
  return B64_VALUES.index(ch)

def b64_to_int(value):
  result = 0

  # Iterate over each character in the Base64 string
  for ch in value:
      result <<= 6  # Shift left by 6 bits
      result |= value_of(ch)  # OR with the Base64 value of the character

  return result

def int_to_b64(value, length=4):
    """
    Converts an integer to a Base64 string of a specified length using the custom Base64 set.
    Pads the front with 'A' if necessary to achieve the desired length.

    Parameters:
        value (int): The integer to convert.
        length (int): The desired length of the Base64 string.

    Returns:
        str: The Base64 string representation of the integer, padded to the specified length.
    """
    if value < 0 or value >= (1 << (6 * length)):  # Ensure the integer fits in the specified length
        raise ValueError(f"Integer value out of range for {length} Base64 characters")

    # Convert integer to Base64 characters
    b64_string = ""
    for _ in range(length):
        b64_string = B64_VALUES[value & 0x3F] + b64_string  # Get last 6 bits and prepend character
        value >>= 6  # Shift value right by 6 bits for the next character

    # If the resulting string is shorter than the desired length, pad with 'A' at the front
    return b64_string.rjust(length, "A")


def calc_pad_bits(byte_array, alignment = 24):
    """
     Calculate the pad bits needed to a particular alignment.  
        Keri/cesr is 24  (3*8): 
          - https://trustoverip.github.io/tswg-keri-specification/#cesr-encoding
          - https://kentbull.com/2024/09/22/keri-series-understanding-self-addressing-identifiers-said/ 
                >> section "24 bit boundary – from Base64"
    """
    # get bits in byte_arr
    bit_num = len(byte_array) * 8
    # get the pad bits needed based on num of bits in byte array
    nhm = nearest_higher_multiple(bit_num, alignment)
    return nhm - bit_num
  
  
def pad_byte_array(byte_array, num_bits, bit_value=0):
    # ensure bit_value is either 0 or 1
    if bit_value not in (0, 1):
        raise ValueError("bit_value must be 0 or 1")

    # calculate full bytes and remaining bits to pad
    full_bytes, remaining_bits = divmod(num_bits, 8)

    # create the full byte padding
    pad_byte = 0xFF if bit_value == 1 else 0x00
    padding = bytes([pad_byte]) * full_bytes

    # if there are remaining bits to pad
    if remaining_bits > 0:
        # make a partial byte for the remaining bits
        partial_byte = (0xFF >> (8 - remaining_bits)) if bit_value == 1 else 0x00
        partial_byte <<= (8 - remaining_bits)
        padding += bytes([partial_byte])

    # concatenate the padding and the original byte array
    return padding + byte_array
  

def byte_array_to_urlsafe_base64(byte_array):
    # encode the byte array to a Base64 string
    base64_str = base64.urlsafe_b64encode(byte_array).decode('utf-8')
    return base64_str

  
def substitute_derivation_code(aligned, deriv_code, padded):
  # each base64 is 6 bits. 
  # calc prepended base64 chars and remove, then add derivation code.
  return deriv_code + aligned[padded//6:]

def replace_said_label(d, label, length=44):
    c = d.copy()
    if label not in c:
        return f"ERROR label: {label} does not exist in dict"
    if len(c[label]) > 0 and len(c[label]) %4 == 0:
        c[label] = "#" * len(c[label])
    else:
        c[label] = "#" *length
    return c


def determine_keri_version(stream):
    
    version_1_pattern = r'\{"v":"(KERI|ACDC)[0-9a-f]{2}(JSON|CBOR|MGPK|CESR)[0-9a-f]{6}_"'
    version_1_pattern_compiled = re.compile(version_1_pattern)
    
    version_2_pattern = r'\{"v":"(KERI|ACDC)([A-Za-z0-9_-]{3})(JSON|CBOR|MGPK|CESR)[A-Za-z0-9_-]{4}\."'
    version_2_pattern_compiled = re.compile(version_2_pattern)
    # match_v2 = re.search(version_2_pattern_compiled, v_string_candidate)  
    
    
    if is_bytes(stream):
        stream = stream.decode('utf-8')
    
    stream =  stream.replace(' ', '')

    # thing should start with the version string 
    v_string_candidate = stream[:24]
    
    match_v1 = re.search(version_1_pattern_compiled, v_string_candidate)
    match_v2 = re.search(version_2_pattern_compiled, v_string_candidate)  

    if match_v1 and not match_v2:
        return 1
    if match_v2 and not match_v1:
        return 2
    if match_v2 and match_v1:
        return -1 # this is an error, should never happen
    else:
        return None
        
def collapse(obj, label):
    """
    Recursively collapses nested dictionaries to a specified label if it exists.

    Parameters:
        obj (dict): The dictionary to collapse.
        label (str): The field name to collapse on (e.g., 'id').

    Returns:
        dict: The collapsed dictionary.
    """
    collapsed_obj = {}

    for key, value in obj.items():
        if isinstance(value, dict) and label in value:
            # Collapse to the specified label's value if it exists in the nested dictionary
            collapsed_obj[key] = value[label]
        else:
            # Otherwise, keep the value as-is
            collapsed_obj[key] = value

    return collapsed_obj
        
def get_version_string_info(v_string, version=1):

    """
    Parses a version string according to the specified version format for KERI/ACDC standards.

    This function extracts details from a version string based on the CESR specification 
    (https://trustoverip.github.io/tswg-cesr-specification/#version-string-field). It supports 
    two versions of the version string format, each with specific terminators and fields.

    Parameters:
        v_string (str or bytes): The version string to parse, formatted as either:
             - VERSION 1: `PPPPvvKKKKllllll_` (17 characters, ending with `_`)
                - PPPP: Protocol (e.g., "KERI" or "ACDC")
                - vv: Version in lowercase hexadecimal notation (major/minor)
                - KKKK: Serialization kind (e.g., "JSON", "CBOR", "MGPK", "CESR")
                - llllll: Size, an integer in lowercase hexadecimal notation
                - Terminator: `_`

            - VERSION 2: `PPPPVVVKKKKBBBB.` (16 characters, ending with `.`)
                - PPPP: Protocol (e.g., "KERI" or "ACDC")
                - VVV: Version (keri Base64-like notation, e.g., "CAA" for 2.00)
                - KKKK: Serialization kind (e.g., "JSON", "CBOR", "MGPK", "CESR")
                - BBBB: Size, an integer encoded in Base64 (use `b64_to_int` for decoding)
                - Terminator: `.`
           
        version (int, optional): Specifies the keri Major version format to parse. 
            Valid options are:
            - 1: For VERSION 1 format.
            - 2: For VERSION 2 format.
            Defaults to 1.

    Returns:
        dict: A dictionary with parsed components of the version string:
            - 'protocol' (str): The protocol identifier (e.g., "KERI", "ACDC").
            - 'version' (str): The version, formatted as a dot-separated string 
                (e.g., "2.00" for VERSION 2).
            - 'kind' (str): The serialization type (e.g., "JSON", "CBOR").
            - '_size' (str): The size field as a string (exact characters from v_string).
            - 'size' (int): The decoded size value as an integer.

    Raises:
        ValueError: If an unrecognized `version` is provided or if `v_string` is not a valid 
                    string or bytes representation.

    Example:
        >>> get_version_string_info('{"v":"ACDC200JSONAAhK."}', version=2)
        {'protocol': 'ACDC', 'version': '2.00', 'kind': 'JSON', '_size': 'AAhK', 'size': 2122}

    Notes:
        - For VERSION 1, hexadecimal size values are converted using `int(_, 16)`.
        - For VERSION 2, Base64 size values are converted using `b64_to_int`.
    """

    
    KNOWN_VERSIONS = [1,2,-1]
    if version not in KNOWN_VERSIONS:
         raise ValueError(f"Unrecognized version: '{version}'. Valid options are: {KNOWN_VERSIONS}")
    
    if not is_string(v_string):
        v_string = v_string.decode()
    
    v_string = v_string.replace('"', '')
    ## detect version from stop delim
    if version == -1:
        if v_string.endswith('.'):
            version = 2
        elif v_string.endswith('_'):
            version = 1
        else:
            raise ValueError(f"Unrecognized version: '{version}'. {v_string}")
    if version == 1:
        stop_delim = v_string.index('_')

        _protocol = v_string[0:4]
        _version = v_string[4:6]
        _kind = v_string[6:10]
        _size = v_string[10:stop_delim]
        _size_length =int(_size, 16)
    

    elif version == 2:
        stop_delim = v_string.index('.')

        _protocol = v_string[0:4]
        _version = '.'.join(str(value_of(c)) for c in v_string[4:7])
        _kind = v_string[7:11]
        _size = v_string[11:stop_delim]
        _size_length =b64_to_int(_size)
    return {
      'protocol': _protocol,
      'version': _version,
      'kind': _kind, # serial
      '_size': _size, # digits
      'size': _size_length
    }


def is_dict(obj):
    return isinstance(obj, dict)

def build_version(data, protocol, kind = 'JSON', major=1, minor=0):
    if not is_bytes(data) and not is_string(data) and is_dict(data):
        _data = dict_to_said_str(data)
    elif is_bytes(data):
        _data = data
    elif is_string(data):
        _data = data.encode()
    
    length = len(_data)

    if len(protocol) != 4:
        raise ValueError(f"protocol must be 4 characters: {protocol}: {len(protocol)}")

    if major == 2:
        # PPPPVVVKKKKBBBB.
        major_rep = int_to_b64(major)[-1]
        minor_rep = int_to_b64(minor)[:-2]

        if len(str(minor_rep)) < 2:
            minor_rep = 'A' + minor_rep
        version_rep = major_rep + minor_rep
        size = int_to_b64(length)
        if len(size) < 4:
            size = 'A' * (4 - len(size)) + size

        return f"{protocol}{version_rep}{kind}{size}."
    
        
    else:
        #  version 1
        # PPPPvvKKKKllllll_
        if major == -1:
            major = 1
        major_rep = hex(major)[2:]
        
        minor_rep = hex(minor)[2:]
        version_rep = major_rep + minor_rep
        size = f"{length:06x}"
        return f"{protocol}{version_rep}{kind}{size}_"
    


def vIsFirst(data, key='v'):
    """
    Checks if the specified key is the first key in the dictionary.

    Parameters:
        data (dict): The dictionary to check.
        key: The key to check if it's at index 0. Defaults to 'v'.

    Returns:
        bool: True if the specified key is the first key, False otherwise.
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")
    
    keys = list(data.keys())
    return keys[0] == key if keys else False

def mapPathsToLabel(data, label='d'):
    """
    Recursively finds paths to all leaves with a specified label in a nested dictionary or list.

    Parameters:
        data (dict or list): The input nested structure.
        label (str): The target label to locate within the nested structure.

    Returns:
        list of list: A list of paths to each occurrence of the specified label.
    """
    paths = []

    def recursive_find(value, current_path=[]):
        # If it's a dictionary, check each key-value pair
        if isinstance(value, dict):
            for key, sub_value in value.items():
                new_path = current_path + [key]
                if key == label:
                    # Add the path as a list if the key matches the target label
                    paths.append(new_path)
                else:
                    # Otherwise, keep traversing deeper
                    recursive_find(sub_value, new_path)
        # If it's a list, traverse each index
        elif isinstance(value, list):
            for index, item in enumerate(value):
                recursive_find(item, current_path + [index])

    # Start recursive search from the root
    recursive_find(data)
    # Sort paths by depth (deepest paths first)
    paths.sort(key=lambda x: len(x), reverse=True)
    return paths


def getNestedObjectAndParent(data, path):
    """
    Retrieves a nested object and its parent from a dictionary or list by following a path represented by a list of keys.

    Parameters:
        data (dict or list): The dictionary or list to traverse.
        path (list): A list of keys/indices representing the path to the nested object.

    Returns:
        tuple: (parent, current) where:
            - current is the nested object if the path exists.
            - parent is the dictionary or list containing the final key or index in the path, or None if the path is not fully valid.
            - If any key in the path is not found, returns (None, None).
    """
    current = data
    parent = None

    for key in path:
        if isinstance(current, dict) and key in current:
            parent = current
            current = current[key]
        elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
            parent = current
            current = current[key]
        else:
            # If the path is invalid, return (None, None)
            return None, None

    return parent, current

def replaceNestedObject( data:dict, path:list, new_obj):
    """
    Replaces a nested object within a dictionary or list with a new object, based on a specified path,
    without compacting any part of the structure.

    Parameters:
        data (dict or list): The original data (dictionary or list) to modify.
        path (list): A list of keys/indices representing the path to the nested object to replace.
        new_obj: The new object to insert at the specified path.

    Returns:
        bool: True if replacement was successful, False otherwise.
    """
    current = data
    for key in path[:-1]:  # Traverse to the parent of the target location
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
            current = current[key]
        else:
            # Path is not valid, return False to indicate no replacement was made
            return False

    # Replace the target object if the final key/index exists in the current structure
    final_key = path[-1]
    if isinstance(current, dict) and final_key in current:
        current[final_key] = new_obj
    elif isinstance(current, list) and isinstance(final_key, int) and 0 <= final_key < len(current):
        current[final_key] = new_obj
    else:
        # If path is invalid for replacement, return False
        return False

    return True

def deepcopy(data:dict):
        """
        Recursively creates a deep copy of a dictionary or list structure.

        Parameters:
            data (dict, list): The original dictionary or list to deep copy.

        Returns:
            A deep copy of the input data.
        """
        if isinstance(data, dict):
            # Recursively deep copy each key-value pair in the dictionary
            return {key: deepcopy(value) for key, value in data.items()}
        elif isinstance(data, list):
            # Recursively deep copy each element in the list
            return [deepcopy(element) for element in data]
        else:
            # For primitive types (int, str, float, etc.), return the value directly
            return data

def equal_in_list(e, _list):
    for i in _list:
        if e == i:
            return True
    return False

def get_said(data, label='d', version=None, ):
    d2 = replace_said_label(data, label)
    vFirstFlag = False
    # print(d2)
    if 't' in  d2 and equal_in_list(d2['t'], ['icp', 'dip', 'vcp']):
        d2 =  replace_said_label(d2, 'i')

    ## calc and get version string if there
    if 'v' in data and vIsFirst(data):
        data_byte_str = dict_to_said_str(data)
        if version == None:
            version = determine_keri_version(data_byte_str)
        if d2['v'].startswith('ACDC'):
            proto_string = 'ACDC'
        else:
            proto_string = 'KERI'
        v_field = build_version(data, proto_string, 'JSON', version, 0)
        d2['v'] = v_field
        


    blake3_byte_arr = blake3_256_from_dict(d2)
    to_pad = calc_pad_bits(blake3_byte_arr, 24)
    aligned_arr = pad_byte_array(blake3_byte_arr, to_pad, 0)
    b64_digest = byte_array_to_urlsafe_base64(aligned_arr)
    said = substitute_derivation_code(b64_digest, 'E', to_pad)
    
    d2[label] = said
    ## REPLACE 'i' on icp, dip, vcp
    if 't' in  d2 and equal_in_list(d2['t'], ['icp', 'dip', 'vcp']):
        d2['i'] = said
        
    return said, d2, said==data[label]

def saidify(sad, label='d', version= -1):
    """
    Calculates and injects SAID values for specified paths within a nested dictionary (SAD) structure.
    Produces both compacted and non-compacted versions of the SAD.

    Parameters:
        sad (dict): The source nested dictionary (SAD) to process.
        code (str): The digest type code used for SAID derivation.
        kind (str): Serialization format to override the SAD's 'v' field if specified.
        label (str): Field name used to locate and collapse structures.
        ignore (list): Optional list of fields to exclude from SAID calculations.

    Returns:
        dict: Contains 'paths', 'sads', 'saiders', 'compact', and 'non_compact' versions of the SAD.
    """
    # print('version', version)
    this_version = -1
    if 'v' in sad:
        v_obj = get_version_string_info(sad['v'], -1)
        this_version = v_obj['version'][0]
        
    version_1_said_calc, _ = get_blake3_256_said(sad, label, False)
    # print(sad[label])
    if str(version).startswith('1') :
        return version_1_said_calc, this_version
    
    def pathJoin(a):
        return '.'.join(map(str, a))

    paths = mapPathsToLabel(sad, label=label)  # Map paths to the specified label
    non_compact = deepcopy(sad)#.copy()
    compact = deepcopy(sad)#.copy()
    sads = {}
    saiders = {}
    

    for path in paths:
        parent, current = getNestedObjectAndParent(compact, path)

        if parent is None or current is None:
            continue

        # Calculate SAID for the current object
        if label in parent:
            _sad = get_said(parent, label=label, version = version)
        else:
            _sad = parent
        
        saiders[pathJoin(path)] = _sad[0]
        sads[pathJoin(path[:-1])] = _sad[1]
        
        # Update `non_compact` only at the specific field level
        replaceNestedObject(non_compact, path, _sad[0])
        if path == [label]:
            if 't' in  non_compact and equal_in_list(non_compact['t'], ['icp', 'dip', 'vcp']):
                non_compact['i'] = _sad[0]
        
        # For `compact`, replace the entire nested structure as per SAID path requirements
        if len(path[:-1]) > 0:
            replaceNestedObject(compact, path[:-1], _sad[0])
        else:
            compact = _sad[1]
    # print(paths)
    # print('-'*88)
    # print(non_compact)
    # print('-'*88)
    t= 'ACDC'
    if 'v' in non_compact:
        if  'KERI' in non_compact['v']:
            print("8"*88)
            t = 'KERI'
        else: 
            t = "ACDC"

        ## TODO replace major here with version number
        non_compact_v = build_version(non_compact, t, kind = 'JSON', major=version, minor=0)
        non_compact['v'] = non_compact_v
        # print('non_compact_v', non_compact_v)

        compact_v = build_version(compact, t, kind = 'JSON', major=version, minor=0)
        # print('compact_v', compact_v)

        compact['v'] = compact_v

    # calc final
    # print('compact')
    # pp.pprint(compact)
    final_said = compact[label]
    # print('final_said', final_said)
    non_compact[label] = final_said

    # print('compact')
    # pp.pprint(compact)
    return {
        'final_said': compact[label],
        'version_1_said_calc': version_1_said_calc,
        'paths': paths,
        'sads': sads,
        'saiders': saiders,
        'compact': compact,
        'non_compact': non_compact,
        'said': compact[label],
        'paths': paths,
        'major_version_detected': this_version
    }


def get_blake3_256_said(data, label, debug=False):
    _data2 = replace_said_label(data, label)
    blake3_byte_arr = blake3_256_from_dict(_data2, debug)
    to_pad = calc_pad_bits(blake3_byte_arr,24)
    aligned_arr = pad_byte_array(blake3_byte_arr, to_pad, 0)
    b64_digest = byte_array_to_urlsafe_base64(aligned_arr)
    said = substitute_derivation_code(b64_digest, 'E', to_pad)
    return said, None