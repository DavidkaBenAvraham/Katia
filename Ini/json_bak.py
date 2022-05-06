import json

def loads(self , file):
    path = f'''{self.path_root}\\Ini\\{file}''' 
    with open(path, 'r') as f:
        data = json.loads(f.read())
    return data
