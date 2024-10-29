import utils

# python main.py path/to/your/file1.json label1 path/to/your/file2.json label2

if __name__ == "__main__":
    # Check if a file path is provided
    data = utils.load_json_from_cli()

    ## check said of each
    for c in data:

        label = c['label']
        _data = c['data']
        said_value = _data[label]
        # said = utils.get_blake3_256_said(_data, label, True)
        said = utils.get_blake3_256_said(_data, label)
        print('*'*88) 
        print(utils.center_text(' '+ c['file_path']+' ', 88,'-'))
        print('calc said:\t', said,)
        print('data said:\t',  _data[label])
        print('match:\t\t', said == _data[label])




