import os
import utils

def run_said_analysis(directory, label="d"):
    """
    Analyzes all JSON files in the specified directory, calculates the SAID, and compares it with the expected value.

    Parameters:
        directory (str): The path to the directory containing JSON files.

    Returns:
        None
    """
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            
            # Simulate the same behavior as main.py
            data = utils.load_json_from_file(file_path)
            # label = data.get('label')
            if not label:
                print(f"Warning: No label found in {filename}")
                continue
            
            # _data = data.get('data', {})
            said_value = data.get(label)
            
            if not said_value:
                print(f"Warning: No SAID value found in {filename}")
                continue
            
            said = utils.get_blake3_256_said(data, label)
            print('*' * 88)
            print(utils.center_text(f' {file_path} ', 88, '-'))
            print('match:\t\t', said == said_value)
            print('data said:\t', said_value)
            print('calc said:\t', said)

def test_acdcs():
    """
    Tests all JSON files in the tests/acdcs directory.
    """
    print("Running SAID analysis for ACDCs:")
    run_said_analysis('../tests/acdcs')

def test_schemas():
    """
    Tests all JSON files in the tests/schemas directory.
    """
    print("Running SAID analysis for Schemas:")
    run_said_analysis('../tests/schemas', "$id")

if __name__ == "__main__":
    print('_'*88)
    test_acdcs()
    print('_'*88)
    test_schemas()
