'''
#################################################################################

   Класс товара
   
#################################################################################
'''

import pandas as pd
import json
import sys
import os
import importlib
import datetime
import time

from logger import Log
from ini_files import Ini
import suppliers


import execute_json as jsn


class Product(Log):

    def __init__(self,lang):
        #super().__init__()
        self.lang = lang
        self.ini = Ini()

        self.fields = dict(jsn.loads(self.ini.ini_path/f'''prestashop_product_fields.json'''))
        self.combinations = dict(jsn.loads(self.ini.ini_path/f'''prestashop_product_combinations_fields.json'''))
        self.prestashop_product_combinations_synonyms = jsn.loads(self.ini.ini_path/f'''prestashop_product_combinations_sysnonyms_{lang}.json''')
        
        pass
    pass

    def skip_row(self, word):
        '''
        Проверка по словарю синонимов 
        '''
        for w in self.prestashop_product_combinations_synonyms["skip"]:
            if str(word).rfind(w) >-1 : return False
        return True
    
    
    
        

