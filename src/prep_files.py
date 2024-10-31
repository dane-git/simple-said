import os 
import utils

def prepare_json_files(directory, overwrite=True):
    out_directory = directory[:]
    backup_directory = None
    if not overwrite:
        backup_directory = utils.create_backup_directory(directory)
    
     
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            
            data = utils.load_json_from_file(file_path)
            data_no_whitespace = utils.dict_to_said_str(data)
            out_file = directory + '/' + filename
            if backup_directory is not None:
                utils.copy_file(file_path, backup_directory)
            with open(out_file, 'w') as f:
                f.write(data_no_whitespace)
                print(f'{out_file} written')



prepare_json_files('../tests/acdcs', False)
