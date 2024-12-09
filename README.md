# SAID Calculator

This project is a Python-based tool for calculating Self-Addressing Identifiers (SAIDs) as defined in the [KERI spec](https://trustoverip.github.io/tswg-keri-specification/).  

## Purpose
Simply to attempt to understand the specification and it's implementation. 

## Features

- Calculate SAID based on inputs following KERI's hashing method. Currently only implement and default to blake3 256.  
- SAID Calculation: Generate SAIDs for data structures, including nested components.  
- Compact/Non-Compact Representations: Process SADs into compact or non-compact forms, supporting flexible data management.  
- Partial Decompaction: Reveal specific parts of a compacted SAD structure selectively, preserving privacy for other components.  


## CLI Example usage
`python main.py -i ../tests/acdcs/ecr-authorization-vlei-credential_e.json  -i ../tests/acdcs/ecr-authorization-vlei-credential.json -v 2  -i ../tests/schemas/qualified-vLEI-issuer-vLEI-credential.json  -v 2`


### 1\. **`saidify`**
```python
saidify(sad, label='d', version=-1, compactify=False)
```

**Description**: Processes a Self-Addressing Data (SAD) structure to calculate and integrate SAIDs. Handles nested components recursively and produces both compact and non-compact representations.

**Key Parameters**:
- `sad` (dict): The SAD structure to process.
- `label` (str): The field name used for SAID storage (default: `'d'`).
- `version` (int): The version to use (inferred if `-1`).
- `compactify` (bool): If `True`, generates a fully compact representation. 
                If the major version is 2, then is set to `True`.

**Returns** (compactified) : A dictionary with details such as:

- `final_said` (str): The calculated SAID for the compact representation.
- `version_1_said_calc` (str): SAID calculated for version 1 (if applicable).
- `paths` (list): Paths to fields where SAIDs were calculated.
- `sads` (dict): Non-compact SAD structures with updated SAIDs at specific paths.
- `saiders` (dict): Calculated SAIDs for individual paths in the SAD.
- `compact` (dict): The compacted SAD with integrated SAIDs.
- `non_compact` (dict): The non-compacted SAD with integrated SAIDs.
- `said` (str): The final SAID of the compact representation.
- `major_version_detected` (int): The major version number detected from the SAD.
- `label`: the said label.   

**Returns** (non-compactified): A tuple (said, updated_ked)

**Notes**:

- Automatically handles versioning when `version=-1`.
- Can compactify anything on the said label if `compactify=True`.

* * *

### 2\. **`get_said`**

```python
get_said(data, label='d', version=None)
```

**Description**: Calculates the SAID for a given data structure using the BLAKE3 hash algorithm. Updates the data structure with the SAID and ensures compatibility with specific message types (`icp`, `dip`, `vcp`).

**Key Parameters**:

- `data`: The data structure for SAID calculation.
- `label`: The field name where the SAID is stored.
- `version`: Optional version string for construction.

**Returns**: A tuple:

- `said`: The calculated SAID.
- `d2`: The updated data structure.
- `is_unchanged`: Whether the calculated SAID matches the existing value.

**Notes**:

- Handles optional versioning.
- Updates the identifier (`i`) field for certain message types.

* * *

### 3\. **`construct_partial`**

```python
construct_partial(paths, sads, label)
```

**Description**: Constructs a partial decompacted version of a SAD structure, selectively revealing nested components based on specified paths.

**Key Parameters**:

- `paths`: A list of paths to nested elements to reveal.
- `sads`: A dictionary of compacted SADs (from `saidify`).
- `label`: The field name used as the SAID label.

**Returns**: A partially decompacted SAD with revealed content for the specified paths. (pass in all the paths for a fully decompacted SAD)

#### Example:
```python
to_reveal = [['e'], ['r', 'Purpose']]
partial = construct_partial(to_reveal, saidified['sads'], saidified['label'])

```
#### Result
```python
{
  'v': 'ACDC10JSON00AAJ9.',
  'd': 'EBtlmHmvTAaT4Fk7OOLz8Lbj0-RRk-CcuAWJqqcM8zUW',
  'i': 'did:keri:EmkPreYpZfFk66jpf3uFv7vklXKhzBrAqjsKAn2EDIPM',
  'e': { 'd': 'ELklZ5xoxJV9w2mEantpo58a76OMp5Cby2S0gk2gU41F',
         'other': 'ENZyhiv9penkbqBqblRpBYTznwf3h84uHh93s_e77A7t'},
  'r': { 'd': 'EGP6QI5LL1X9unCUymIwtQRjp9p4r_loUgKdymVpn_VG',
         'Purpose': { 'd': 'EOF9OZMZudCRFDU_AmJWY7Py3KdazRsGnbEz-QIQ7HJj',
                      'l': 'One-time admittance of Issuer by Issuee to eat '
                           'at place on date as specified in Attribute '
                           'section.'}}
}

```






























































































