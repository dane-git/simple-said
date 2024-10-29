import json
import blake3
import base64

import json
import sys
import os

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
    # if (len(sys.argv) - 1) % 2 != 0:
    #     print("Usage: python main.py <path1> <label1> <path2> <label2> ...")
    #     sys.exit(1)

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

def get_blake3_256_said(data, label, debug=False):
    _data2 = replace_said_label(data, label)
    blake3_byte_arr = blake3_256_from_dict(_data2, debug)
    to_pad = calc_pad_bits(blake3_byte_arr,24)
    aligned_arr = pad_byte_array(blake3_byte_arr, to_pad, 0)
    b64_digest = byte_array_to_urlsafe_base64(aligned_arr)
    said = substitute_derivation_code(b64_digest, 'E', to_pad)
    return said