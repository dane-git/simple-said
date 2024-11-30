# SAID Calculator

This project is a Python-based tool for calculating Self-Addressing Identifiers (SAIDs) as defined in the [KERI spec](https://trustoverip.github.io/tswg-keri-specification/).  

## Purpose
Simply to attempt to understand the specification and it's implementation. 

## Features

- Calculate SAID based on inputs following KERI's hashing method. Currently only implement and default to blake3 256.


## Example usage
`python main.py -i ../tests/acdcs/ecr-authorization-vlei-credential_e.json  -i ../tests/acdcs/ecr-authorization-vlei-credential.json -v 2  -i ../tests/schemas/qualified-vLEI-issuer-vLEI-credential.json  -v 2`




## Test Data
## Test data
Current test data grabbed from: https://github.com/WebOfTrust/vLEI