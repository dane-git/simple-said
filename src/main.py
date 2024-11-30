import utils
import pprint
pp = pprint.PrettyPrinter(indent=2, sort_dicts=False)

# python main.py path/to/your/file1.json label1 path/to/your/file2.json label2

if __name__ == "__main__":
    # Check if a file path is provided
    # data = utils.load_json_from_cli()
    args = utils.parse_input_args()

    print("args")
    # print(args)
    data = []
    # print(data)
    # for d in data:
    #     print(d)
    
    compactify = False
    print()
    ## check said of each
    for c in args:
        print(c.keys())
        print('fn', c['file_name'])
        print('label', c['label'])
        print('verison', c['version'])
        # continue

        label = c['label']
        _data = c['data']
        version = int(c['version'])
        print(version)
        said_value = _data[label]
        # said = utils.get_blake3_256_said(_data, label, True)
        if str(version).startswith == '2':
            compactify = True
        said  = utils.saidify(_data, label, version, compactify=compactify)
        print('*'*88) 
        print(utils.center_text(' '+ c['file_path']+' ', 88,'-'))
        print('calc said:\t', said,)
        print('data said:\t',  _data[label])
        print('match:\t\t', said == _data[label])
        # pp.pprint(_)




