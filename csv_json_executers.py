import pandas as pd
import csv
# как работать с csv https://python-scripts.com/import-csv-python

from ini_files_dir import Ini
import os
import sys


'''                 CSV ЧАСТЬ      здесь все плохо реализовано  '''


''' ------------------ НАЧАЛО -------------------------- '''
def write(self , data  , path_to_file) ->bool:

    try:
       # self.df.to_csv(path_to_file, sep=';', encoding='utf-8' ,index=False)
       # self.print(f''' Данные экспортированы в файл
       #{path_to_file} ''')
       pd.DataFrame(data).to_csv(path_to_file, sep=';', encoding='utf-8' ,index=False) 
       return True
    
    except Exception as ex:
        print(ex)
        return False
        ''' ------------------ КОНЕЦ  -------------------------- '''



''' ------------------ НАЧАЛО -------------------------- '''
def csv_files_combination_by_suppliers():
    #объединение файлов csv разных категорий товаров в один общий
    pass

    ''' ------------------ КОНЕЦ  -------------------------- '''




'''                          JSON   ЧАСТЬ           '''


     
from pathlib import Path
import json as json
from logger import Log

from exceptions_handler import ExceptionsHandler as EH

''' ------------------ НАЧАЛО -------------------------- ''' 
#@print
def loads(path:Path )-> dict :
    ''' получаю объект Path - не str! '''
    with path.absolute().open(encoding='utf-8') as f:
            data = json.loads(f.read())
    return data
    ''' ------------------ КОНЕЦ  -------------------------- '''


''' ------------------ НАЧАЛО -------------------------- '''  
def dump(data , path:Path):
    if str(type(data)).find('list')>-1: 
        data = json.dumps(data).replace('[','{').replace(']','}')
    with path.absolute().open('w',encoding='utf-8') as f:
            json.dump(data ,f)
    ''' ------------------ КОНЕЦ  -------------------------- '''


''' ------------------ НАЧАЛО -------------------------- '''  
def html2json(html:str)->json:
    pass
    ''' ------------------ КОНЕЦ  -------------------------- '''
