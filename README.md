# SAID Calculator

This project is a Python-based tool for calculating Self-Addressing Identifiers (SAIDs) as defined in the [KERI spec](https://trustoverip.github.io/tswg-keri-specification/).  

## Purpose
Simply to attempt to understand the specification and it's implementation. 

## Features

- Calculate SAID based on inputs following KERI's hashing method. Currently only implement and default to blake3 256.  
- SAID Calculation: Generate SAIDs for data structures, including nested components.  
- Compact/Non-Compact Representations: Process SADs into compact or non-compact forms, supporting flexible data management.  
- Partial Decompaction: Reveal specific parts of a compacted SAD structure selectively, preserving privacy for other components.  

## **Installation**

To install the library:

```bash
git clone https://github.com/dane-git/simple-said.git
cd simple-said
pip install .
```
<!-- TODO
## CLI Example usage
`python main.py -i ../tests/acdcs/ecr-authorization-vlei-credential_e.json  -i ../tests/acdcs/ecr-authorization-vlei-credential.json -v 2  -i ../tests/schemas/qualified-vLEI-issuer-vLEI-credential.json  -v 2` -->


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

- `said_v1` (str): SAID calculated for version 1 (if applicable).
- `said` (str): The calculated SAID for the compact representation.
- `paths` (list): Paths to fields where SAIDs were calculated.
- `sads` (dict): compact SAD structures with updated SAIDs at specific paths.
- `saiders` (dict): Calculated SAIDs for individual paths in the SAD.
- `compact` (dict): The compacted final SAD with integrated SAIDs.
- `non_compact` (dict): The non-compacted SAD with integrated SAIDs.
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
- `sad`: The updated data structure.
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

## Example:
- First get the results from saidify

#### Original non compactified
```python
from simple_said import saidify

example = { 
  'v': 'ACDCCAAJSONAAVE.',
  'd': 'EEc0llA5ATA0LqgD3NacFddX0P_Q8has1CW5yKtYsFq5',
  'i': 'did:keri:EmkPreYpZfFk66jpf3uFv7vklXKhzBrAqjsKAn2EDIPM',
  's': 'EGGeIZ8a8FWS7a646jrVPTzlSkUPqs4reAXRZOkogZ2A',
  'a': { 'd': 'EFQF1FMPvppOYH5mREvhtpeVIOyIA5qUR8yoDXlPjdrr',
         'i': 'did:keri:EpZfFk66jpf3uFv7vklXKhzBrAqjsKAn2EDIPmkPreYA',
         'date': '2022-08-22T17:50:09.988921+00:00',
         'place': { 'd': 'EFe4t4vP0C7e-tThgEy3HxyDRa62p9oTDxGJkqjkbfK8',
                    'u': '0A8xHxiskgz5jJ8ZYtEfnBt_',
                    'a': 'GoodFood Restaurant, 953 East Sheridan Ave, Cody WY '
                         '82414 USA'}},
  'e': { 'd': 'ELklZ5xoxJV9w2mEantpo58a76OMp5Cby2S0gk2gU41F',
         'other': { 'd': 'ENZyhiv9penkbqBqblRpBYTznwf3h84uHh93s_e77A7t',
                    'n': 'EIl3MORH3dCdoFOLe71iheqcywJcnjtJtQIYPvAu6DZA'}},
  'r': { 'd': 'EGP6QI5LL1X9unCUymIwtQRjp9p4r_loUgKdymVpn_VG',
         'Assimilation': { 'd': 'EBRRwxQlC6b57S_7mnH-p51N3lUcgO8AAcQrgl_FTuPo',
                           'l': 'Issuee hereby explicitly and unambiguously '
                                'agrees to NOT assimilate, aggregate, '
                                'correlate, or otherwise use in combination '
                                'with other information available to the '
                                'Issuee, the information, in whole or in part, '
                                'referenced by this container or any '
                                'containers recursively referenced by the edge '
                                'section, for any purpose other than that '
                                'expressly permitted by the Purpose clause.'},
         'Purpose': { 'd': 'EOF9OZMZudCRFDU_AmJWY7Py3KdazRsGnbEz-QIQ7HJj',
                      'l': 'One-time admittance of Issuer by Issuee to eat at '
                           'place on date as specified in Attribute section.'}
        }
}

saidified = saidify.saidify(example)
```

### Parial Disclosures Example

#### Partial reveal 1
```python
to_reveal = [['r','Assimilation'], ['r', 'Purpose']]
partial_1 = saidify.construct_partial(to_reveal, saidified ['sads'], saidified ['label'])
pp.pprint(partial_1)
```
output:
```python
{ 'v': 'ACDCCAAJSONAAPC.',
  'd': 'EEc0llA5ATA0LqgD3NacFddX0P_Q8has1CW5yKtYsFq5',
  'i': 'did:keri:EmkPreYpZfFk66jpf3uFv7vklXKhzBrAqjsKAn2EDIPM',
  's': 'EGGeIZ8a8FWS7a646jrVPTzlSkUPqs4reAXRZOkogZ2A',
  'a': 'EFQF1FMPvppOYH5mREvhtpeVIOyIA5qUR8yoDXlPjdrr',
  'e': 'ELklZ5xoxJV9w2mEantpo58a76OMp5Cby2S0gk2gU41F',
  'r': { 'd': 'EGP6QI5LL1X9unCUymIwtQRjp9p4r_loUgKdymVpn_VG',
         'Assimilation': { 'd': 'EBRRwxQlC6b57S_7mnH-p51N3lUcgO8AAcQrgl_FTuPo',
                           'l': 'Issuee hereby explicitly and unambiguously '
                                'agrees to NOT assimilate, aggregate, '
                                'correlate, or otherwise use in combination '
                                'with other information available to the '
                                'Issuee, the information, in whole or in part, '
                                'referenced by this container or any '
                                'containers recursively referenced by the edge '
                                'section, for any purpose other than that '
                                'expressly permitted by the Purpose clause.'},
         'Purpose': { 'd': 'EOF9OZMZudCRFDU_AmJWY7Py3KdazRsGnbEz-QIQ7HJj',
                      'l': 'One-time admittance of Issuer by Issuee to eat at '
                           'place on date as specified in Attribute section.'}
        }
}
```
#### Partial reveal 2
```python
to_reveal = [['r','Assimilation'], ['r', 'Purpose'], ['a']]
partial_2 = saidify.construct_partial(to_reveal, saidified ['sads'], saidified ['label'])
pp.pprint(partial_2)
```
output:
```python
{ 'v': 'ACDCCAAJSONAARl.',
  'd': 'EEc0llA5ATA0LqgD3NacFddX0P_Q8has1CW5yKtYsFq5',
  'i': 'did:keri:EmkPreYpZfFk66jpf3uFv7vklXKhzBrAqjsKAn2EDIPM',
  's': 'EGGeIZ8a8FWS7a646jrVPTzlSkUPqs4reAXRZOkogZ2A',
  'a': { 'd': 'EFQF1FMPvppOYH5mREvhtpeVIOyIA5qUR8yoDXlPjdrr',
         'i': 'did:keri:EpZfFk66jpf3uFv7vklXKhzBrAqjsKAn2EDIPmkPreYA',
         'date': '2022-08-22T17:50:09.988921+00:00',
         'place': 'EFe4t4vP0C7e-tThgEy3HxyDRa62p9oTDxGJkqjkbfK8'},
  'e': 'ELklZ5xoxJV9w2mEantpo58a76OMp5Cby2S0gk2gU41F',
  'r': { 'd': 'EGP6QI5LL1X9unCUymIwtQRjp9p4r_loUgKdymVpn_VG',
         'Assimilation': { 'd': 'EBRRwxQlC6b57S_7mnH-p51N3lUcgO8AAcQrgl_FTuPo',
                           'l': 'Issuee hereby explicitly and unambiguously '
                                'agrees to NOT assimilate, aggregate, '
                                'correlate, or otherwise use in combination '
                                'with other information available to the '
                                'Issuee, the information, in whole or in part, '
                                'referenced by this container or any '
                                'containers recursively referenced by the edge '
                                'section, for any purpose other than that '
                                'expressly permitted by the Purpose clause.'},
         'Purpose': { 'd': 'EOF9OZMZudCRFDU_AmJWY7Py3KdazRsGnbEz-QIQ7HJj',
                      'l': 'One-time admittance of Issuer by Issuee to eat at '
                           'place on date as specified in Attribute section.'}
        }
}
```

#### Partial reveal 3
```python
to_reveal = [['r','Assimilation'], ['r', 'Purpose'], ['a', 'place']]
partial_3 = saidify.construct_partial(to_reveal, saidified ['sads'], saidified ['label'])
pp.pprint(partial_3)
```
output:
```python
{ 'v': 'ACDCCAAJSONAATO.',
  'd': 'EEc0llA5ATA0LqgD3NacFddX0P_Q8has1CW5yKtYsFq5',
  'i': 'did:keri:EmkPreYpZfFk66jpf3uFv7vklXKhzBrAqjsKAn2EDIPM',
  's': 'EGGeIZ8a8FWS7a646jrVPTzlSkUPqs4reAXRZOkogZ2A',
  'a': { 'd': 'EFQF1FMPvppOYH5mREvhtpeVIOyIA5qUR8yoDXlPjdrr',
         'i': 'did:keri:EpZfFk66jpf3uFv7vklXKhzBrAqjsKAn2EDIPmkPreYA',
         'date': '2022-08-22T17:50:09.988921+00:00',
         'place': { 'd': 'EFe4t4vP0C7e-tThgEy3HxyDRa62p9oTDxGJkqjkbfK8',
                    'u': '0A8xHxiskgz5jJ8ZYtEfnBt_',
                    'a': 'GoodFood Restaurant, 953 East Sheridan Ave, Cody WY '
                         '82414 USA'}},
  'e': 'ELklZ5xoxJV9w2mEantpo58a76OMp5Cby2S0gk2gU41F',
  'r': { 'd': 'EGP6QI5LL1X9unCUymIwtQRjp9p4r_loUgKdymVpn_VG',
         'Assimilation': { 'd': 'EBRRwxQlC6b57S_7mnH-p51N3lUcgO8AAcQrgl_FTuPo',
                           'l': 'Issuee hereby explicitly and unambiguously '
                                'agrees to NOT assimilate, aggregate, '
                                'correlate, or otherwise use in combination '
                                'with other information available to the '
                                'Issuee, the information, in whole or in part, '
                                'referenced by this container or any '
                                'containers recursively referenced by the edge '
                                'section, for any purpose other than that '
                                'expressly permitted by the Purpose clause.'},
         'Purpose': { 'd': 'EOF9OZMZudCRFDU_AmJWY7Py3KdazRsGnbEz-QIQ7HJj',
                      'l': 'One-time admittance of Issuer by Issuee to eat at '
                           'place on date as specified in Attribute section.'}
        }
}
```


### 4\.**`disclosure_by_saids`**

#### **Description**

The `disclosure_by_saids` function selectively expands (decompacts) specific SAIDs (Self-Addressing Identifiers) within a Self-Addressing Data (SAD) structure. It is used to partially reveal specific components of a compacted SAD while keeping the rest of the structure in its compact form.

This function is particularly useful for controlled disclosure of data, where only selected parts of a SAD are expanded based on a given list of SAIDs.

* * *

#### **Parameters**

- **`expanded`** *(dict)*:
    
    - A fully or partially expanded SAD structure that serves as the base for disclosure.
- **`saids`** *(list of str)*:
    
    - A list of SAIDs (Self-Addressing Identifiers) to expand within the SAD.
- **`label`** *(str, optional)*:
    
    - The label field in the SAD that identifies SAIDs. Defaults to `'d'`.

* * *

#### **Returns**

- **`exposed`** *(dict)*:
    - A partially decompactified (partially disclosed) SAD structure where the specified SAIDs are expanded.

```python

agg_expanded = { 
  'v': 'ACDCCAAJSONAAXR.',
  'd': 'ENlHA-EkJGkwIHhqKDn0BSTZ9tT-dYRqCq-2G-aSMNqk',
  'u': '0AHcgNghkDaG7OY1wjaDAE0q',
  'i': 'EAqjsKFk66jpf3uFv7An2EDIPMvklXKhmkPreYpZfzBr',
  'rd': 'EMwsxUelUauaXtMxTfPAMPAI6FkekwlOjkggtymRy7x',
  's': 'EAXRZOkogZ2A46jrVPTzlSkUPqGGeIZ8a8FWS7a6s4re',
  'A': [ { 'd': 'EC9mAmY9RI140l3CX_6EK6aDl5lXns6TM65Ho00pM4nm',
           'u': '0AqHcgNghkDaG7OY1wjaDAE0',
           'i': 'did:keri:EpZfFk66jpf3uFv7vklXKhzBrAqjsKAn2EDIPmkPreYA'},
         { 'd': 'EFLx0eeyvz_kBgKuWl60Rh7rHXJiiXE9mUw7qtolLgTL',
           'u': '0AG7OY1wjaDAE0qHcgNghkDa',
           'class': 'Chemistry',
           'quarter': '2022-1',
           'pass': True,
           'score': { 'd': 'EHdeZq0uF37SWzr_ng93XdcOpeKIsHUjyWOqEF7GIZ8C',
                      'u': '0AtzfJAh4ZY_aOEMjfquKB3H',
                      'value': '83.4'}},
         { 'd': 'EALtrm1Lhoa4PJcpmvwxpXzrE04GGRxsXWlK8EVTs3jF',
           'u': '0AghkDaG7OY1wjaDAE0qHcgN',
           'name': 'Jane Doe'}],
  'r': { 'd': 'ENJaQBhwUr5PibfWi_DIajpd6MDVc39BopFlIBfAe-RN',
         'Assimilation': { 'd': 'ENlj2cOTvH40XMV5uKdFP85LNEoBtPDSWkLwrr0GvmXQ',
                           'u': '0AAxNda_GP6MeB_hDrQ-03RD',
                           'l': 'Issuee hereby explicitly and unambiguously '
                                'agrees to NOT assimilate, aggregate, '
                                'correlate, or otherwise use in combination '
                                'with other information available to the '
                                'Issuee, the information, in whole or in part, '
                                'referenced by this container or any '
                                'containers recursively referenced by the edge '
                                'section, for any purpose other than that '
                                'expressly permitted by the Purpose clause.'},
         'Purpose': { 'd': 'EIBWPzwdEYVM0MN6MJ4H0xr9V8MiOQsXegwvZoSZcgJo',
                      'u': '0AXqUyDnOdyNq-NKI5CqdSrk',
                      'l': 'One-time admittance of Issuer by Issuee to eat at '
                           'place on date as specified in Attribute section.'}}}

partial_agg= saidify.disclosure_by_saids(agg_expanded, 
                    ['EIBWPzwdEYVM0MN6MJ4H0xr9V8MiOQsXegwvZoSZcgJo',
                     'EFLx0eeyvz_kBgKuWl60Rh7rHXJiiXE9mUw7qtolLgTL'])
pp.pprint(partial_agg )
```
output:
```python
{ 'v': 'ACDCCAAJSONAANj.',
  'd': 'ENlHA-EkJGkwIHhqKDn0BSTZ9tT-dYRqCq-2G-aSMNqk',
  'u': '0AHcgNghkDaG7OY1wjaDAE0q',
  'i': 'EAqjsKFk66jpf3uFv7An2EDIPMvklXKhmkPreYpZfzBr',
  'rd': 'EMwsxUelUauaXtMxTfPAMPAI6FkekwlOjkggtymRy7x',
  's': 'EAXRZOkogZ2A46jrVPTzlSkUPqGGeIZ8a8FWS7a6s4re',
  'A': [ 'EC9mAmY9RI140l3CX_6EK6aDl5lXns6TM65Ho00pM4nm',
         { 'd': 'EFLx0eeyvz_kBgKuWl60Rh7rHXJiiXE9mUw7qtolLgTL',
           'u': '0AG7OY1wjaDAE0qHcgNghkDa',
           'class': 'Chemistry',
           'quarter': '2022-1',
           'pass': True,
           'score': 'EHdeZq0uF37SWzr_ng93XdcOpeKIsHUjyWOqEF7GIZ8C'},
         'EALtrm1Lhoa4PJcpmvwxpXzrE04GGRxsXWlK8EVTs3jF'],
  'r': { 'd': 'ENJaQBhwUr5PibfWi_DIajpd6MDVc39BopFlIBfAe-RN',
         'Assimilation': 'ENlj2cOTvH40XMV5uKdFP85LNEoBtPDSWkLwrr0GvmXQ',
         'Purpose': { 'd': 'EIBWPzwdEYVM0MN6MJ4H0xr9V8MiOQsXegwvZoSZcgJo',
                      'u': '0AXqUyDnOdyNq-NKI5CqdSrk',
                      'l': 'One-time admittance of Issuer by Issuee to eat at '
                           'place on date as specified in Attribute section.'}}}
```































































































