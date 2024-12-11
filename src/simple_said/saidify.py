import json
import blake3
import base64
import datetime
import sys
import re
import shutil
import pprint
import os


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
    # print(95)
    # print(file_list)
    for idx in range(len(file_list)):
        try:
            f = os.path.basename(file_list[idx]['file_name'])
            # print(101,f)
            
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
        major = int(v_string[4], 16)
        minor = int(v_string[5], 16)
        
        _protocol = v_string[0:4]
        _version = str(major) + '.' + str(minor)
        _kind = v_string[6:10]
        _size = v_string[10:stop_delim]
        _size_length =int(_size, 16)
    

    elif version == 2:
        stop_delim = v_string.index('.')
        minorv = 0
        for c in v_string[5:7]:
            minorv += value_of(c)
        
        _protocol = v_string[0:4]
        _version = str(value_of(v_string[4])) + '.' + str(minorv)
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

def set_v_field_length(data: dict, major):
    len_data = deepcopy(data)
    if major == 1:
        len_data['v'] = '#'*17
    elif major == 2:
        len_data['v'] = '#'*16
    return len(dict_to_said_str(len_data))

def build_version(data, protocol, kind = 'JSON', major=1, minor=0):
    length = None
    if not is_bytes(data) and not is_string(data) and is_dict(data):
        length = set_v_field_length(data, major)
        
    elif is_bytes(data):
        data = data.decode('utf-8')
        data = json.load(data)
        length = set_v_field_length(data, major)
        
    elif is_string(data):
        data = json.load(data)
        length = set_v_field_length(data, major)
    
    

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

def find_value_in_dict(data, target, current_path=()):
    """
    Recursively find the path to a target value in a dictionary.
    The value can occur as a key or a value, even in nested structures or lists.

    Parameters:
    ----------
    data : dict | list
        The dictionary or list to search.
    target : Any
        The value to search for.
    current_path : tuple, optional
        The current path being traversed (default: empty tuple).

    Returns:
    -------
    tuple | None
        The path to the target value as a tuple, or None if not found.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            # Check if the key matches the target
            if key == target:
                return current_path + (key,)
            # Check if the value matches the target
            if value == target:
                return current_path + (key,)
            # Recurse into nested structures
            if isinstance(value, (dict, list)):
                result = find_value_in_dict(value, target, current_path + (key,))
                if result is not None:
                    return result

    elif isinstance(data, list):
        for index, item in enumerate(data):
            # Check each item in the list
            if item == target:
                return current_path + (index,)
            # Recurse into nested structures
            if isinstance(item, (dict, list)):
                result = find_value_in_dict(item, target, current_path + (index,))
                if result is not None:
                    return result
    return None

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


## Simple version full said.  no recursion
def get_said(data, label='d', version=None ):
    """
    Calculate the Self-Addressing Identifier (SAID) for a given data structure.

    This function generates a SAID using the BLAKE3 hash of the provided data. It replaces
    specific labels in the data structure for processing and applies appropriate derivation
    codes. For certain message types (`icp`, `dip`, `vcp`), it ensures the identifier (`i`)
    field is also updated with the calculated SAID.

    Parameters:
    ----------
    data : dict
        The data structure for which the SAID is calculated.
    label : str, optional
        The field name in the data where the SAID is stored. Defaults to 'd'.
    version : str, optional
        Version string to use when constructing the SAID. If None, it will be determined
        automatically.

    Returns:
    -------
    tuple:
        - said (str): The calculated SAID as a base64-encoded string.
        - d2 (dict): The updated data structure with the SAID included.
        - is_unchanged (bool): Whether the calculated SAID matches the existing value 
          under the specified label in the original data.

    Notes:
    -----
    - For messages of type `icp`, `dip`, or `vcp`, the SAID is applied to the `i` field
      in addition to the specified label.
    - The function handles optional version information, constructing a version field 
      based on the protocol (`KERI` or `ACDC`) and the detected or supplied version.
    """
    sad = replace_said_label(data, label)
    if is_dict(sad) and  't' in  sad and equal_in_list(sad['t'], ['icp', 'dip', 'vcp']):
        sad =  replace_said_label(sad, 'i')

    ## calc and get version string if there
    if is_dict(sad) and 'v' in data and vIsFirst(data):
        data_byte_str = dict_to_said_str(data)
        if version == None:
            version = determine_keri_version(data_byte_str)
        if sad['v'].startswith('ACDC'):
            proto_string = 'ACDC'
        else:
            proto_string = 'KERI'
        v_field = build_version(data, proto_string, 'JSON', version, 0)
        sad['v'] = v_field
        

    blake3_byte_arr = blake3_256_from_dict(sad)
    to_pad = calc_pad_bits(blake3_byte_arr, 24)
    aligned_arr = pad_byte_array(blake3_byte_arr, to_pad, 0)
    b64_digest = byte_array_to_urlsafe_base64(aligned_arr)
    said = substitute_derivation_code(b64_digest, 'E', to_pad)
    
    sad[label] = said
    ## REPLACE 'i' on icp, dip, vcp
    if 't' in  sad and equal_in_list(sad['t'], ['icp', 'dip', 'vcp']):
        sad['i'] = said
        
    return said, sad, said==data[label]

def saidify(sad, label='d', version= -1, compactify=False):
    """
    Process a Self-Addressing Data (SAD) structure to calculate and integrate SAIDs.

    This function takes a SAD structure and processes it recursively to calculate 
    Self-Addressing Identifiers (SAIDs) for nested components, producing both compact 
    and non-compact representations. It also determines the version and type (e.g., 
    ACDC, KERI) of the SAD and updates the version fields as necessary.

    Parameters:
    ----------
    sad : dict
        The Self-Addressing Data (SAD) structure to be processed.
    label : str, optional
        The field name in the data used for the SAID (default is 'd').
    version : int, optional
        The version number to use for SAID calculations. If -1, it is inferred from 
        the SAD's `v` field (default is -1).
    compactify : bool, optional
        If True, generates a fully compact representation; if False, the output will depend
         on the detected major version.

    Returns:
    -------
    (compactified)
    dict
        A dictionary with the following keys:
        - 'said_v1' (str): SAID calculated for version 1 (if applicable).
        - 'said' (str): The calculated SAID for the compact representation.
        - 'paths' (list): Paths to fields where SAIDs were calculated.
        - 'sads' (dict): (tuple[path]): SAD: compact SAD structures with updated SAIDs at specific paths.
        - 'saiders' (dict): Calculated SAIDs for individual paths in the SAD.
        - 'compact' (dict): The compacted SAD with integrated SAIDs.
        - 'non_compact' (dict): The non-compacted SAD with integrated SAIDs.
        - 'major_version_detected' (int): The major version number detected from the SAD.
        - 'label': the said label

    Notes:
    -----
    - If the SAD's `v` field is present, the function extracts version information 
      and uses it unless a specific version is supplied.
    - For version 1 and `compactify=False`, the function skips additional compact 
      processing and directly returns the version 1 SAID.
    - The function distinguishes between compact and non-compact processing based on 
      nested SAID paths, integrating them where required.
    """

    this_version = -1
    sad_ = deepcopy(sad)
    if 'v' in sad_:
        v_obj = get_version_string_info(sad_['v'], -1)
        this_version = v_obj['version'][0]
        if version == -1:
            version = int(this_version)
    version_1_said_calc, v = get_blake3_256_said(sad_, label, False)
    if str(version).startswith('1') and compactify == False:
        sad_[label] = version_1_said_calc
        sad_['v'] = v
        return version_1_said_calc, sad_
    
    def pathJoin(a):
        return '.'.join(map(str, a))

    paths = mapPathsToLabel(sad_, label=label)  # Map paths to the specified label
    non_compact = deepcopy(sad_)#.copy()
    compact = deepcopy(sad_)#.copy()
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
        sads[tuple(path)] = _sad[1]
        
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

        compact_v = build_version(compact, t, kind = 'JSON', major=version, minor=0)

        compact['v'] = compact_v

    compact_said, _, _ = get_said(compact, label=label)
    compact[label] = compact_said
    final_said = compact[label]

    non_compact[label] = final_said

    return {
        'said_v1': version_1_said_calc,
        'said': compact[label],
        'paths': paths,
        'sads': sads,
        'saiders': saiders,
        'compact': compact,
        'non_compact': non_compact,
        'major_version_detected': this_version,
        'label': label
    }

def build_version_string(data, major = None):
    if 'v' in data and vIsFirst(data):
        if major is None:
            major = determine_keri_version(dict_to_keri_byte_str(data))
        v_info = get_version_string_info(data['v'], major)
        
        return build_version(
            data, v_info['protocol'], 
            v_info['kind'], 
            major=major, 
            minor=int(''.join(v_info['version'].split('.')[1:]))
        )
    return None
# determine_keri_version(stream)
def get_blake3_256_said(data, label, debug=False):
    data_2 = replace_said_label(data, label)
    v_string = build_version_string(data)
    if v_string is not None:
        data_2['v'] = v_string
    blake3_byte_arr = blake3_256_from_dict(data_2, debug)
    to_pad = calc_pad_bits(blake3_byte_arr,24)
    aligned_arr = pad_byte_array(blake3_byte_arr, to_pad, 0)
    b64_digest = byte_array_to_urlsafe_base64(aligned_arr)
    said = substitute_derivation_code(b64_digest, 'E', to_pad)
    return said, v_string
  
def update_v2string_length(ked):
    _raw = dict_to_keri_byte_str(ked)
    _size = len(_raw)
    size_b64 = int_to_b64(_size)
    v_string = ked['v'][:-5] + size_b64 + '.'
    return v_string

def update_v1string_length(ked):
    _raw = dict_to_keri_byte_str(ked)
    _size = len(_raw)
    size = f"{_size:06x}"
    v_string = ked['v']
    v_string = v_string[:10] + size + '_'
    return v_string
# ==================================== SIMPLE DECOMPACTIFY ( iterative ) =================================================

## construct a partial, given a list of paths and all the compact sads.
def construct_partial(paths, sads, label):
    """
    Construct a partial decompacted version of a Self-Addressing Data (SAD) structure.

    This function selectively reveals nested components of a compacted SAD structure 
    based on the specified paths. It progressively decompacts parts of the SAD while 
    keeping the rest compact. This is useful for revealing specific parts of a SAD 
    without exposing the full data structure.

    Parameters:
    ----------
    paths : list of lists
        A list of paths, where each path is a list of keys that identify a nested
        element in the SAD. The paths specify which parts of the compacted SAD
        to reveal.
    sads : dict
        A dictionary of compacted SADs, typically generated from the `saidify` function.
        The keys represent paths to nested components, and the values are the corresponding
        SAD objects.
    label : str
        The field name in the SAD used as the SAID label (e.g., 'd').

    Returns:
    -------
    dict
        A partially decompacted SAD structure, where the specified paths have been
        expanded to reveal their nested content.

    Notes:
    -----
    - The function retrieves the root SAD from the `sads` dictionary using the label field.
    - The paths are sorted by length to ensure hierarchical decompaction.
    - For each path, the SAD is progressively decompacted by revealing the nested
      structure up to the specified depth.
    - If a path ends in the label (e.g., `['e', 'other', 'd']`), it is treated as equivalent
      to `['e', 'other']`.

    Example:
    --------
    Given the following SADs from `saidify` and paths to reveal:
    >>> to_reveal = [['e'], ['r', 'Purpose']]
    >>> partial = construct_partial(to_reveal, saidified['sads'], saidified['label'])

    The resulting `partial` SAD will look like this:
    >>> pp.pprint(partial)
    { 'v': 'ACDC10JSON00AAJ9.',
      'd': 'EBtlmHmvTAaT4Fk7OOLz8Lbj0-RRk-CcuAWJqqcM8zUW',
      'i': 'did:keri:EmkPreYpZfFk66jpf3uFv7vklXKhzBrAqjsKAn2EDIPM',
      's': 'EGGeIZ8a8FWS7a646jrVPTzlSkUPqs4reAXRZOkogZ2A',
      'a': 'EAlRl3pCPbtOWUz_O4xWpEJJrsMhQwjmIwLmXtxWz-fu',
      'e': { 'd': 'ELklZ5xoxJV9w2mEantpo58a76OMp5Cby2S0gk2gU41F',
             'other': 'ENZyhiv9penkbqBqblRpBYTznwf3h84uHh93s_e77A7t'},
      'r': { 'd': 'EGP6QI5LL1X9unCUymIwtQRjp9p4r_loUgKdymVpn_VG',
             'Purpose': { 'd': 'EOF9OZMZudCRFDU_AmJWY7Py3KdazRsGnbEz-QIQ7HJj',
                          'l': 'One-time admittance of Issuer by Issuee to eat '
                               'at place on date as specified in Attribute '
                               'section.'}}}
    """
    # GET ROOT KED ( COMAPCITIFED ) 
    for sad in sads:
        sad_path = sad
        if sad_path[0] == label:
            root_ked = deepcopy(sads[sad])

    # sort from shortest to longest, just because
    paths = sorted(paths, key=len)
    for path in paths:
        root_ked = simple_decompactify(path, sads, label,root_ked)
    return root_ked
    
def vIsFirst(data, key='v'):
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")
    
    keys = list(data.keys())
    return keys[0] == key if keys else False
    
def simple_decompactify(path, all_sads, label,root_ked = {}):
    """
    Rebuilds a nested structure recursively by adding compactified versions
    of SADs along the specified path.

    Parameters:
        path (list): The path to decompactify to.
        all_sads (list): A list of Sadder instances.
        root_ked (dict): the root ked to build on top of. default will fill to the compact ked
    Returns:
        dict: The modified root object with the specified path decompactified.
    """    
    if root_ked == {}:
        for sad in all_sads:
            sad_path
            if label == sad_path[0]:
                rk = deepcopy(all_sads[sad])
                root_ked = deepcopy(rk)
    match_path = []
    for key in path:
        # go to current spot
        match_path.append(key)
        if key == label:
            if vIsFirst(root_ked):
                v_version = 1 if root_ked['v'].endswith('_') else 2
                if v_version == 1:
                    root_ked['v'] = update_v1string_length(root_ked)
                else:
                    root_ked['v']  = update_v2string_length(root_ked)
            return root_ked
        current_obj = root_ked
        for p in match_path:
          if p in current_obj:
            if isinstance(current_obj[p], (dict, list)):
              current_obj  = current_obj[p]
              continue
            else:
              ## find sad that matches:
              for sad in all_sads:
                sad_path = sad
                if sad_path[:-1] ==  tuple(match_path):
                  current_obj[p] = deepcopy(all_sads[sad])
                  break
              continue
          else:
            # print(p, match_path)
            for sad in all_sads:
              sad_path = sad
              if sad_path[:-1] ==  tuple(match_path):
                current_obj[p] = deepcopy(all_sads[sad])
                break
    if vIsFirst(root_ked):
        root_ked['v']  = update_v2string_length(root_ked)
    return root_ked                


def disclosure_by_saids(expanded, saids, label='d'):
    """
    Partially discloses a Self-Addressing Data (SAD) structure by selectively expanding specified SAIDs.

    This function takes a fully or partially expanded SAD, a list of SAIDs to expand, and a label field.
    It finds the paths to the specified SAIDs in the SAD, compacts the SAD using the `saidify` function,
    and reconstructs a partially expanded version using the specified SAIDs.

    Parameters:
    ----------
    expanded : dict
        The fully or partially expanded SAD structure to process.
        This is the base data structure from which the specified SAIDs will be selectively expanded.
    saids : list of str
        A list of SAIDs (Self-Addressing Identifiers) to expand within the SAD.
    label : str, optional
        The label field used to identify SAIDs in the SAD (default is 'd').

    Returns:
    -------
    dict
        A partially decompactified SAD structure where the specified SAIDs are expanded.
    """
    paths = []
    for said in saids:
        p = find_value_in_dict(expanded, said)
        if p is not None:
            paths.append(p)
    s = saidify(expanded, label=label, compactify=True)
    sads = s['sads']
    exposed = construct_partial(paths, sads, label)
    return exposed