from simple_said.kutils import (
    replace_said_label,
    is_dict,
    equal_in_list,
    dict_to_keri_byte_str,
    determine_keri_version,
    build_version,
    deepcopy,
    get_version_string_info,
    calc_pad_bits,
    pad_byte_array,
    byte_array_to_urlsafe_base64,
    substitute_derivation_code,
    dict_to_said_str,
    blake3_256_from_dict,
    keri_blake256_data,
    get_blake3_256_said,
    update_v1string_length,
    update_v2string_length,
    v_is_first
    )


import pprint


pp = pprint.PrettyPrinter(indent=2, sort_dicts=False)


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
        


def map_paths_to_label(data, label='d'):
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

def get_nested_object_and_parent(data, path):
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

def replace_nested_object( data:dict, path:list, new_obj):
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
    if is_dict(sad) and 'v' in data and v_is_first(data):
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

    paths = map_paths_to_label(sad_, label=label)  # Map paths to the specified label
    non_compact = deepcopy(sad_)#.copy()
    compact = deepcopy(sad_)#.copy()
    sads = {}
    saiders = {}
    

    for path in paths:
        parent, current = get_nested_object_and_parent(compact, path)

        if parent is None or current is None:
            continue

        # Calculate SAID for the current object
        if label in parent:
            _sad = get_said(parent, label=label, version = version)
        else:
            _sad = parent
        
        saiders[tuple(path)] = _sad[0]
        sads[tuple(path)] = _sad[1]
        
        # Update `non_compact` only at the specific field level
        replace_nested_object(non_compact, path, _sad[0])
        if path == [label]:
            if 't' in  non_compact and equal_in_list(non_compact['t'], ['icp', 'dip', 'vcp']):
                non_compact['i'] = _sad[0]
        
        # For `compact`, replace the entire nested structure as per SAID path requirements
        if len(path[:-1]) > 0:
            replace_nested_object(compact, path[:-1], _sad[0])
        else:
            compact = _sad[1]


    ## TODO Fix, only root level aggregated A field handeled.
    if 'A' in compact:
        
        if isinstance(compact['A'], list):
            all_saids = True
            arr_saids = []
            for elem in compact['A']:
                ## TODO: fix this
                ## unsafe assumption
                if isinstance(elem, str) and len(elem) % 22 == 0:
                    arr_saids.append(elem)
                else:
                    # print(elem, type(elem) ,len(elem) %22)
                    all_saids = False
            if all_saids:
                agg_said = keri_blake256_data(''.join(arr_saids))
                sads[tuple('A')] = agg_said
                for i, e in enumerate(arr_saids):
                    p = ('A',i)
                    sads[p] = e
                    saiders[p] = e
                    paths.append(list(p))
                    
                compact['A'] = agg_said
                _p = tuple('A')
                sads[_p] = agg_said
                saiders[_p] = agg_said
                paths.append(['A'])
    t= 'ACDC'
    if 'v' in non_compact:
        if  'KERI' in non_compact['v']:
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
    
    
    # ## TODO Fix, only root level aggregated A field handeled.
    # has_agg_paths = False
    # for p in paths:
    #     if 'A' in p:
    #         has_agg_paths = True
    # # print(paths)
    # if has_agg_paths:
    #     # print(has_agg_paths)
    #     expanded_agg = []
    #     for p in sads:
    #         if len(p) <= 2 and p[0] == 'A':
    #             expanded_agg.append(sads[p])
            
    #     root_ked['A'] = expanded_agg
    # sort from shortest to longest, just because
    paths = sorted(paths, key=len)
    # print(paths)
    for path in paths:
        # print(path)
        # print(root_ked)
        root_ked = simple_decompactify(path, sads, label,root_ked)
    return root_ked
    

    
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
            sad_path = sad

            if label == sad_path[0]:
                rk = deepcopy(all_sads[sad])
                root_ked = deepcopy(rk)
    match_path = []

    A = None
    for s in all_sads:
        if s == tuple('A'):
            A = all_sads[s]
    for key in path:
        match_path.append(key)
        if key == label:
            if v_is_first(root_ked):
                v_version = 1 if root_ked['v'].endswith('_') else 2
                if v_version == 1:
                    root_ked['v'] = update_v1string_length(root_ked)
                else:
                    root_ked['v']  = update_v2string_length(root_ked)
            return root_ked
        current_obj = root_ked
        for p in match_path:
        #   print(p)
          if p in current_obj:
            if isinstance(current_obj[p], (dict, list)):
              if p == 'A':
                #   print(1200)
                #   print(current_obj)
                  if 'A' in current_obj:
                    #   print(1202)
                      if A in current_obj['A']:
                          current_obj['A'].remove(A)
                  elif A in current_obj:
                    #   print(1206)
                      current_obj.remove(A)
              current_obj  = current_obj[p]
              continue
            else:
            #   print(1212)
              ## find sad that matches:
              for sad in all_sads:
                if p == 'A' and path[-1] != 'A':
                  continue
                sad_path = sad
                if sad_path[:-1] ==  tuple(match_path):
                  current_obj[p] = deepcopy(all_sads[sad])
                  break
              
              continue
          else:
            # print(605)

            # print(p, match_path)
            ## TODO FIX: HACKY A field fill.
            if p == '...':
                for sad in all_sads:
                    if sad == tuple(match_path):
                        current_obj[match_path[-2]] = all_sads[sad]
                        break
            
            for sad in all_sads:
              sad_path = sad
              if sad_path[:-1] ==  tuple(match_path):
                if not isinstance(current_obj[p], dict):
                    if 'A' in path:
                        # print(1235)
                        if A in current_obj:
                            current_obj.remove(A)
                    current_obj[p] = deepcopy(all_sads[sad])
                else:
                    current_obj = current_obj[p]
                break
        
    if v_is_first(root_ked):
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
    not_found = []
    for said in saids:
        p = find_value_in_dict(expanded, said)
        if p is not None:
            paths.append(p)
        if p is None:
            not_found.append(said)
    
    # s = saidify(expanded, label=label, compactify=True)
    s = recursive_saidify(expanded, label=label)#, compactify=True)
    if len(not_found):
        # pass
        for nf in not_found:
            for p in s['saiders']:
                if s['saiders'][p] == nf:
                    paths.append(p)
                    
    def exists_in_tuple_list(_list, value):
        for tup in _list:
            if value in tup:
                return True
        return False
    
    def find_start_indexes_tuple_list(_list, value):
        start_indexes = []
        for tup in _list:
            if value in tup:
                i = tup.index(value)
                if i not in start_indexes:
                    start_indexes.append(i)
        return start_indexes
    
    sads = s['sads']
    if exists_in_tuple_list(paths, 'A') and not exists_in_tuple_list(paths, '...'):
        expanded_A_paths = []
        start_indexes = find_start_indexes_tuple_list(paths, 'A')
        for s in start_indexes:
            for p in sads:
                # print(p, len(p) >= s+2)

                if len(p) >= s+2:
                    if p[s] == 'A' and p[s+1] == '...':
                        expanded_A_paths.append(p)
                
        paths = paths + expanded_A_paths
            
        
    # print(paths)
   
    exposed = construct_partial(paths, sads, label)
    return exposed

def recursive_saidify(sad, label, debug=False):
        """
        Recursively replaces the 'label' values with SAIDs and collapses special 'A' fields 
        such that all 'A' fields are resolved before calculating parent SAIDs.

        Parameters:
            sad (dict): The input dictionary.
            label (str): The target field to replace with SAIDs.
            debug (bool): Enables debug output.

        Returns:
            saids: (dict: (tuple: path) said string): Updated dictionary with SAID replacements and 'A' field collapses.
            sads: (dict: (tuple: path)) SADs, fully compacted.
            report: (dict {path: tuple (valid:bool, calculated said: str, original said: str)})
            paths: (list of tuples) paths of all the SAIDs and or SADs
            valid: (bool) True if all calculated saids match saids provided in data.
            compact: (dict): most compact form of SAD possible.
        """
        sads = {}        # SAID mappings
        saiders = {}     # SAID raw data
        report = {}      # SAID valid report by path
        paths = []       # all sad - saider paths
        valid = True     # True if all saids match calculation
        

        def process_special_a_field(data, path):
            """Collapse an 'A' field into its concatenated hash."""
            if isinstance(data, list):
                exp_path = path + ('...',)
                sads[exp_path] = data
                paths.append(exp_path)
                concatenated = ''.join(data)
                hashed = keri_blake256_data(concatenated)  # Replace with the correct hash function
                sads[path] = hashed
                return hashed
            return data

        def recurse(data, path=()):
            """Post-order recursive function to process 'A' fields and SAIDs."""
            if isinstance(data, dict):
                updated = {}

                # Process children first (post-order traversal)
                for key, value in data.items():
                    current_path = path + (key,)
                    updated[key] = recurse(value, current_path)

                # Collapse the 'A' field, if present
                if "A" in updated:
                    special_path = path + ("A",)
                    updated["A"] = process_special_a_field(updated["A"], special_path)
                    if debug:
                        print(f"Collapsed 'A' field at path {special_path}: {updated['A']}")

                # Replace the label and calculate its SAID
                if label in updated:
                    said = get_said(updated, label)
                    path = path + (label,)
                    paths.append(path)
                    sads[path] = said[1]
                    saiders[path] = said[0]
                    report[path] = (said[-1], said[0], updated[label])
                    if said[-1] == False:
    
                        nonlocal valid
                        valid = False
                    updated = said[0]  # Replace the entire dict with its SAID version
                    if debug:
                        print(f"Replaced label '{label}' at path {path} with SAID: {said[1]}")

                return updated

            elif isinstance(data, list):
                return [recurse(item, path + (i,)) for i, item in enumerate(data)]

            else:
                return data

        # Start processing with a deepcopy of the input
        _sad = deepcopy(sad)
        updated_data = recurse(_sad)

        return {
            "said": updated_data,
            "sads": sads,
            "saiders": saiders,
            "report": report,
            "paths": paths,
            "valid": valid,
            "compact": sads[(label,)]
        }