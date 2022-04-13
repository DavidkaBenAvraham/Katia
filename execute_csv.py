import pandas as pd
import csv
# как работать с csv https://python-scripts.com/import-csv-python

from Ini import Ini
import os
import sys

def write(self , data , path_to_file):

    #self.df.drop_duplicates()
    
    try:
       # self.df.to_csv(path_to_file, sep=';', encoding='utf-8' ,index=False)
       # self.log(f''' Данные экспортированы в файл
       #{path_to_file} ''')
       pd.DataFrame(data).to_csv(path_to_file, sep=';', encoding='utf-8' ,index=False) 
       return True
    
    except Exception as ex:
        #path_to_file = path_to_file + '_'
        self.log(f'''Файл открыт или занят другим процессом! 
        {ex}
        {data}''')
        sys.exit()
        return True


def csv_files_combination_by_suppliers():
    #объединение файлов csv разных категорий товаров в один общий
    pass
