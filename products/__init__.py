'''
#################################################################################

                    Класс товара
   
#################################################################################


'''
from pathlib import Path
import pandas as pd
import sys
import os 
import datetime
import time

from ini_files_dir import Ini
from logger import Log
from attr import attrs, attrib, Factory
import pandas as pd
import execute_json as json

@attrs
class Product():
    ''' Всё, что относится к товару
    '''
    
    fields : pd.DataFrame = attrib(init = False, default = None)
    ''' поля товара (для престашоп) '''

    combinations : pd.DataFrame = attrib(init = False , default = None)
    ''' поля комбинаций товаара '''
    
    prestashop_product_combinations_synonyms: pd.DataFrame = attrib(init = False, default = None)
    ''' Уже не помню '''
    
    ini : Ini = attrib(init = False , default = None)
    ''' мне не нравится, чтo ini вызывается не один раз '''

    def __attrs_post_init__(self , *args, **kwards):
        ''' считываю поля товара в датафреймы для дальнейших исследований
        ''' 
        self.ini = Ini()
        
        self.fields =   pd.DataFrame(
                           json.loads(
                                  Path(
                        self.ini.paths.ini_files_dir , f'''prestashop_product_fields.json'''
                              )))

        self.combinations = pd.DataFrame(
                               json.loads(
                                      Path(
                        self.ini.paths.ini_files_dir , f'''prestashop_product_combinations_fields.json'''
                              )))

        self.prestashop_product_combinations_synonyms = pd.DataFrame(
                          json.loads(
                                 Path(
                        self.ini.paths.ini_files_dir , f'''prestashop_product_combinations_sysnonyms_{lang}.json'''
                              )))
        
        pass
    pass


    def skip_row(self, word):
        ''' Проверка по словарю синонимов 
        '''
        for w in self.prestashop_product_combinations_synonyms["skip"]:
            if str(word).rfind(w) >-1 : return False , self.print(f'''{w} найдено''')
        return True , self.print(f'''{w} не найдено''')
    
    