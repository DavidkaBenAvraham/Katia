##@package e-cat.me
# всякие полезности для работы с JSON


from pathlib import Path
import json as json
from logger import Log

from exceptions_handler import ExceptionsHandler as EH

## Документация для функции.
#
# Подробнее.
def loads(path:Path )-> dict :
    ''' получаю объект Path - не str! '''
    with path.absolute().open(encoding='utf-8') as f:
            data = json.loads(f.read())
    return data
## Документация для функции.
#
# Подробнее.
def dump(data , path:Path):
    if str(type(data)).find('list')>-1: 
        data = json.dumps(data).replace('[','{').replace(']','}')
    with path.absolute().open('w',encoding='utf-8') as f:
            json.dump(data ,f)
## Документация для функции.
#
# Подробнее.
def html2json(html:str)->json:
    pass


## Документация для функции.
#
# Подробнее. 
def export(data , format : list = ['json','csv'] , filename : str = None):
    ''' позволяет экспортировать словарь в файл 
    из всех точек выполнения сценариев '''

    export_file_path =  Path(f'''{self.ini.paths.export_dir}''')
       
    if filename == None:
        filename = f'''{self.supplier_prefics}-{self.ini.get_now()}'''


    for frmt in format:
        export_file_path =  Path(export_file_path , f'''{filename}.{frmt}''')
        if frmt == 'json':
            json.dump(data, export_file_path)
        if frmt == 'csv':
            json.write(self, data , export_file_path)

    



