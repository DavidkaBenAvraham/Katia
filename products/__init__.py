'''
#################################################################################

   Класс товара
   
#################################################################################

                    Ini()---------------+
                    |                   |
                    |                   +---    path:Path
                    |                   |           физический адрес программы
                    |                   |           
                    |                   +---    path_str : str
                    |                   |           строка path
                    |                   |           
                    |                   +---    path_ini  : Path
                    |                   |           директория файлов иницилазации программы
                    |                   |           
                    |                   +---    path_ini_str : str
                    |                   |           строка path_ini
                    |                   |           
                    |                   +---    path_path_log_dir : Path
                    |                   |           директория файлов log
                    |                   |           
                    |                   +---    path_export_dir : Path
                    |                   |           директория файлов экспорта
                    |                   |           
                    |                   +---    start_time  : datetime
                    |                   +---    get_now(): datetime
                    |
                    |
                Log(Ini)----------------+
                |                       |
                |                       +---    header()
                |                       |           заголовок HTML лога в котором можно
                |                       |           прописать функции, например, jacascript
                |                       |           сейчас записана функция скрытия свойств
                |                       |           классов и типов в логе
                |                       |           
                |                       +---    screenshot(self , log = object) 
                |                       |
                |                       +---    print(self, log = object, prn_type="jupiter") 
                |                       |       |
                |                       |       \/  
                |                       +---    write_log_to_file(self, log:object)
                |                       |
                |                       +---    logged(method_to_decorate)
                |                       +---    print_attr(self, *o):
                |
        Product(Log)--------------------+
                                        |
                                        +---
'''

import pandas as pd
import json
import sys
import os
import importlib
import datetime
import time

from ini_files import Ini
from logger import Log

import suppliers


import execute_json as jsn


class Product(Log):

    def __init__(self,lang):
        super().__init__()
        self.lang = lang
        
        self.fields = dict(jsn.loads(self.path_ini/f'''prestashop_product_fields.json'''))
        self.combinations = dict(jsn.loads(self.path_ini/f'''prestashop_product_combinations_fields.json'''))
        self.prestashop_product_combinations_synonyms = jsn.loads(self.path_ini/f'''prestashop_product_combinations_sysnonyms_{lang}.json''')
        
        pass
    pass

    def skip_row(self, word):
        '''
        Проверка по словарю синонимов 
        '''
        for w in self.prestashop_product_combinations_synonyms["skip"]:
            if str(word).rfind(w) >-1 : return False , self.print(f'''{w} найдено''')
        return True , self.print(f'''{w} не найдено''')
    
    
    
    def export_to_csv(self:[]):
        df = pd.DataFrame(self)
        pass


