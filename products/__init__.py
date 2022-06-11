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
from strings_formatter import StringFormatter as SF

from ini_files_dir import Ini
from logger import Log
from attr import attrs, attrib, Factory
import pandas as pd
import execute_json as json

@attrs
class Product():
    ''' Всё, что относится к товару csv_json_executers
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
        ''' Плохое , очень плохое решение'''


        
        self.fields = json.loads(Path(self.ini.paths.ini_files_dir , f'''prestashop_product_fields.json'''))

        self.combinations =json.loads(Path(self.ini.paths.ini_files_dir , f'''prestashop_product_combinations_fields.json'''))

        #self.prestashop_product_combinations_synonyms = json.loads(Path(self.ini.paths.ini_files_dir , f'''prestashop_product_combinations_sysnonyms_{lang}.json'''))
        pass
    pass


    def skip_row(self, word):
        ''' Проверка по словарю синонимов 
        '''
        for w in self.prestashop_product_combinations_synonyms["skip"]:
            if str(word).rfind(w) >-1 : return False , self.print(f'''{w} найдено''')
        return True , self.print(f'''{w} не найдено''')
    
    
    def get_product_fields_from_product_page(self,s):
    
        '''
        https://stackoverflow.com/questions/34301815/understand-the-find-function-in-beautiful-soup#_=_
        Here we are also checking for presence of data-value attribute.
        soup.find("span", {"class": "real number", "data-value": True})['data-value']
        '''
        p = Product()

        p.fields["title"] = SF.remove_special_characters(s.driver.title)

        '''
    
             Получаю сырые данные со страницы

        '''

        raw_product_price_supplier = s.driver.find(s.locators['product']['product_price_locator'])
        raw_product_images = ','.join(s.driver.find(s.locators['product']['product_images_locator']))
        raw_product_images_alt = ','.join(s.driver.find(s.locators['product']['product_images_alt_locator']))
        raw_product_sikum = ''.join(s.driver.find(s.locators['product']['product_sikum_locator']))
        combinations = ''.join(s.driver.find(s.locators['product']['product_attributes_locator']))
        raw_product_description = ''.join(s.driver.find(s.locators['product']['product_description_locator']))
        raw_product_mkt_locator = ''.join(s.driver.find(s.locators['product']['product_mkt_locator']))

        p.fields["categories"] = s.current_node["prestashop_category"]

        tiur = formatter.remove_special_characters(f'''{raw_product_description}''')

        p.fields["tiur"] = tiur
        p.fields["sikum"] = formatter.remove_special_characters(f'''{raw_product_sikum}''')

    

        p.fields["img url"] = f'''{raw_product_images}'''
        p.fields["img alt"] = f'''{raw_product_images_alt}'''

        p.fields["mkt"] = f'''{raw_product_mkt_locator}'''
        p.fields["mkt suppl"] = f'''{raw_product_mkt_locator}'''
   
   
        price_supplier = formatter.clear_price(f'''{raw_product_price_supplier}''').strip('[]')

        p.fields["mexir lifney"]=price_supplier
        p.fields["mexir olut"]=price_supplier
        p.fields["mexir le yexida"]=price_supplier

        '''
                        Аттрибуты товара


        =================================================================================================


                                  "Product ID": "",
                                  "Attribute (Name:Type: Position)": "",
                                  "value (Name:Type: Position)": "",
                                  "Supplier reference": "",
                                  "Reference": "",
                                  "EAN13": "",
                                  "UPC": "",
                                  "Wholesale price": "",
                                  "Impact on price": "",
                                  "Ecotax": "",
                                  "Quantity": "",
                                  "Minimal quantity": "",
                                  "Low stock level": "",
                                  "Impact on weight": "",
                                  "Default (0/1)": "",
                                  "Combination available date": "",
                                  "Image position": "",
                                  "Image URLs(x,y,z)": "",
                                  "Image Alt Text(x,y,z)": "",
                                  "shop": "1,2,3,4",
                                  "Advanced Stock Mangment": 0,
                                  "Depends On Stock": 0,
                                  "Warehouse": 0



        '''
        product_attributes(self,p,'div',raw_product_description)



        return p

    pass