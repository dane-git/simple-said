import json
import blake3
import base64

import datetime
import sys
import os
import re
import shutil

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

def load_json_from_cli():
    """
    Reads JSON file paths and labels from command-line arguments and loads each file.

    Returns:
        dict: A dictionary where each label maps to the contents of the corresponding JSON file.

    Raises:
        SystemExit: If the required arguments are missing or if there are errors loading any JSON file.
    """
    # Ensure there’s an even number of arguments (each file has a path and a label)
    if (len(sys.argv) - 1) % 2 != 0:
        print("Usage: python main.py <path1> <label1> <path2> <label2> ...")
        sys.exit(1)

    _data = []

    # Iterate over arguments in pairs (path and label)

    for i in range(1, len(sys.argv), 2):
        data = {}
        file_path = sys.argv[i]
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        # print(i)
        # print(file_path)
        label = sys.argv[i + 1]
        # print(label)
        # Load JSON data for the given file path
        try:
            with open(file_path, 'r') as file:
                o = {'file_path': file_path,
                     'file_name': file_name,
                     'label': label,
                     'data': {}}
                d = json.load(file)

                o['data'] = d
                _data.append(o)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: The file '{file_path}' is not valid JSON.")
            sys.exit(1)

    return _data

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

def replace_said_label(d, label):
    c = d.copy()
    if label not in c:
        return f"ERROR label: {label} does not exist in dict"

    c[label] = "#" * len(c[label])
    return c


def determine_keri_version(stream):
    # pattern for VERSION 1
    version_1_pattern = r'\{"v":"(KERI|ACDC)[0-9a-f]{2}(JSON|CBOR|MGPK|CESR)[0-9a-f]{6}_"'
    version_1_pattern_compiled = re.compile(version_1_pattern)
    
    version_2_pattern = r'\{"v":"(KERI|ACDC)([A-Za-z0-9_-]{3})(JSON|CBOR|MGPK|CESR)[A-Za-z0-9_-]{4}\."'
    version_2_pattern_compiled = re.compile(version_2_pattern)
    # match_v2 = re.search(version_2_pattern_compiled, v_string_candidate)  
    
    # thing should start with the version string 
    
    if is_bytes(stream):
        stream = stream.decode('utf-8').replace(' ', '')
    
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

    
    KNOWN_VERSIONS = [1,2]
    if version not in KNOWN_VERSIONS:
         raise ValueError(f"Unrecognized version: '{version}'. Valid options are: {KNOWN_VERSIONS}")
    
    if not is_string(v_string):
        v_string = v_string.decode()
    
    v_string = v_string.replace('"', '')
    
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
        __version = v_string[4:7]
        _version = ''
        for c in __version:
            _version += str(value_of(c))
            _version += '.'
        _version = _version[:-1]
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

def get_blake3_256_said(data, label, debug=False):
    _data2 = replace_said_label(data, label)
    blake3_byte_arr = blake3_256_from_dict(_data2, debug)
    to_pad = calc_pad_bits(blake3_byte_arr,24)
    aligned_arr = pad_byte_array(blake3_byte_arr, to_pad, 0)
    b64_digest = byte_array_to_urlsafe_base64(aligned_arr)
    said = substitute_derivation_code(b64_digest, 'E', to_pad)
    return said