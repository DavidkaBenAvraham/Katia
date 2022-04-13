import json
def loads(path_to_file):
    #try:
    #    with open(path_to_file, 'r') as f:
    #        data = json.loads(f.read())
    #    return data
    #except Exception as ex:
    #    self.log(f''' Ошибка чтения файла JSON {path_to_file} 
    #        {ex} ''')
    #    return False
    with open(path_to_file, 'r') as f:
            data = json.loads(f.read())
    return data
