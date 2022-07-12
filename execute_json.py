# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia.Tools
# execute_json.py
# всякие полезности для работы с JSON


from pathlib import Path
import json as json
import csv
from logger import Log
import pandas as pd

## Читаю файл из внешнего источника .
# path: путь к файлу 
def loads(path:Path )-> dict :
    ''' получаю объект Path - не str! '''
    with path.absolute().open(encoding='utf-8') as f:
        data = json.loads(f.read())
    return data


## скидываю словарь <b>data</b> в файл <b>path</b>
# dump(data , path).
# <hr>
# data : данные в виде словаря или   списка (?). <br>
# path : путь к файлу.
def dump(data , path:Path):
    if str(type(data)).find('list')>-1: 
        data = json.dumps(data).replace('[','{').replace(']','}')
    with path.absolute().open('w',encoding='utf-8') as f:
            json.dump(data ,f)


## Документация для функции.
def html2json(html:str)->json:
    pass




### экспортирую данные в файл .
# функция позволяет экспортировать словарь в файл <br>
# из всех точек выполнения сценариев 
def export(supplier, data, filename:str = None, format:list = ['json','csv','txt'])->bool:

    export_file_path = Path(f'''{supplier.ini.paths.export_dir}''')
       
    #if filename == None:
    #    filename = f'''-{supplier.supplier_prefics}'''


    filename = f'''-{supplier.supplier_prefics} '''
    

    for frmt in format:
        export_file_path =  Path(export_file_path , f'''{filename}-{supplier.ini.get_now()}.{frmt}''')
        if frmt == 'json':
            json.dump(data, export_file_path)

        if frmt == 'csv':
            df = pd.DataFrame(data)
            df.to_csv(export_file_path , sep = ';' , index=False ,  encoding='utf-8')
           
        if frmt == 'txt': 
            with open(export_file_path, 'w')as txtfile:
                txtfile.write(str(data))
              



