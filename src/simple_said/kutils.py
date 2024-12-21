import json
import blake3
import re
import base64



B64_VALUES = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

def is_bytes(obj):
    return isinstance(obj, bytes)
def is_string(obj):
    return isinstance(obj, str)

def byte_to_bits(byte):
    return format(byte, '08b')
  
def bytes_to_bits(byte_array):
    return ''.join(format(byte, '08b') for byte in byte_array)

def value_of(ch):
    return B64_VALUES.index(ch)

def int_to_bits(i):
    binary_string = format(i, 'b')
    return binary_string

def is_dict(obj):
    return isinstance(obj, dict)

def bits_to_int(bit_string):
    return int(bit_string, 2)
    

def make_bit_string(int_array):

    if not int_array:
        return ""

    # Find the maximum bit length required for the largest number in the array
    max_bits = max(int_array).bit_length()

    # Convert each integer to a binary string of uniform bit length
    #bit_string = ''.join(f"{num:0{max_bits}b}" for num in int_array)
    bit_array = [f"{num:0{max_bits}b}" for num in int_array]

    return  bit_array#, bit_string



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
  

def nearest_higher_multiple(x, n):
    """
     Calculate the nearest higher multiple of n greater than or equal to x
    """
    if x % n == 0:
        return x
    else:
        return ((x // n) + 1) * n



def equal_in_list(e, _list):
    for i in _list:
        if e == i:
            return True
    return False   
 
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

def set_v_field_length(data: dict, major):
    len_data = deepcopy(data)
    if major == 1:
        len_data['v'] = '#'*17
    elif major == 2:
        len_data['v'] = '#'*16
    return len(dict_to_said_str(len_data))


 
 
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
    
def build_version_string(data, major = None):
    if 'v' in data and v_is_first(data):
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

def keri_blake256_data(data):
    if is_dict:
        data = dict_to_keri_byte_str(data)
    if is_string(data):
        data = data.encode()
    blake3_byte_arr = blake3_to_byte_array(data)
    to_pad = calc_pad_bits(blake3_byte_arr,24)
    aligned_arr = pad_byte_array(blake3_byte_arr, to_pad, 0)
    b64_digest = byte_array_to_urlsafe_base64(aligned_arr)
    said = substitute_derivation_code(b64_digest, 'E', to_pad)
    return said

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
    said2 = keri_blake256_data(data_2)
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

def v_is_first(data, key='v'):
    """
    Checks if the specified key is the first key in the dictionary.

    Parameters:
        data (dict): The dictionary to check.
        key: The key to check if it's at index 0. Defaults to 'v'.

    Returns:
        bool: True if the specified key is the first key, False otherwise.
    """

    if not isinstance(data, dict):
        return data
    
    keys = list(data.keys())
    return keys[0] == key if keys else False



def make_bit_str(num, length=8):
    s = f"{num:0{length}b}"
    return s