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
from attr import attrs, attrib, Factory
import pandas as pd

from strings_formatter import StringFormatter

from ini_files_dir import Ini
from logger import Log
import execute_json as json




@attrs
class Product():
    ''' Всё, что относится к товару csv_json_executers
    '''
    
    s  = attrib(kw_only = True, default = None)   

    fields : pd.DataFrame = attrib(init = False, default = None)
    ''' поля товара (для престашоп) '''

    combinations : pd.DataFrame = attrib(init = False , default = None)
    ''' поля комбинаций товара '''

    attributes : pd.DataFrame = attrib(init = False , default = None)
    ''' поля комбинаций товара '''


  
    def __attrs_post_init__(self , *args, **kwards):
        ''' считываю поля товара в датафреймы для дальнейших исследований
        ''' 
       
        
        self.fields = json.loads(Path(self.s.ini.paths.ini_files_dir , f'''prestashop_product_fields.json'''))

        self.combinations =json.loads(Path(self.s.ini.paths.ini_files_dir , f'''prestashop_product_combinations_fields.json'''))


   
    def grab_product_page(self) -> dict:
        _d = self.s.driver
        #_d.scroll(3)
        _ : dict = self.s.locators['product']
        field = self.fields

        def get_id():
            try:field['id'] = _d.find(_['product_id_locator'])
            except Exception as ex: field['id'] = None, print(ex)

        def get_title():
            try: field['product_title'] = _d.find(_['product_title_locator'])
            except Exception as ex: field['product_title'] = None, print(ex)

        def get_price():
            try:
                _price = _d.find(_['product_price_locator'])
                field['product_price'] = formatter.clear_price(_price)
            except Exception as ex: field['product_price'] = None, print(ex)

        def get_shipping():
            try:
                field['product_shipping'] = _d.find(_['product_shipping_locator'])
            except Exception as ex: field['shipping'] = None, print(ex)
  
        def get_images():
            try:
                _images = _d.find(_['product_images'])
                for k,v in _images.items():
                       field['img url'] += f''' {v}, '''
                       field['img alt'] += f''' {k}, '''
            
            except Exception as ex: field['product_images'] = None, print(ex)

        def get_attributes():
            try:
                field['product_attributes'] = _d.find(_['product_attributes_locator'])
            
            except Exception as ex: field['product_attributes'] = None, print(ex)

        def get_qty():
            try:
                _qty = _d.find(_['product_qty-locator'])
                field['qty'] = formatter.clear_price(_qty)
            
            except Exception as ex: field['qty'] = None, print(ex)

        def get_byer_protection():
            try:
                field['product_byer_protection'] = _d.find(_['product_byer_protection_locator'])
            except Exception as ex: field['product_byer_protection'] = None, print(ex)

        def get_description():
            try:
                field['product_description'] = _d.find(_['product_description_locator'])
            except Exception as ex: field['product_description'] = None, print(ex)

        def get_specification():
            try:
                field['product_specification'] = _d.find(_['product_specification_locator'])
            except Exception as ex: field['product_specification'] = None, print(ex)
        def get_customer_reviews():
            try:
                field['product_customer_reviews'] = _d.find(_['product_customer_reviews_locator'])
            except Exception as ex: field['product_customer_reviews'] = None, print(ex)


        ''' fill fields '''
        get_id(),
        get_title(),
        get_price(),
        get_shipping(),
        get_images(),
        get_attributes(),
        get_qty(),
        get_byer_protection(),
        get_description(),
        get_specification(),
        get_customer_reviews()
        
        return self
