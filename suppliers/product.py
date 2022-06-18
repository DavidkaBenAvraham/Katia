# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia.Product
#Documentation for module
  
from pathlib import Path
import pandas as pd
import sys
import os 
import datetime
import time
from attr import attrs, attrib, Factory
import pandas as pd

from strings_formatter import StringFormatter
formatter = StringFormatter()

from ini_files_dir import Ini
from logger import Log
import execute_json as json



##@package Katia.Product
## Документация для класса
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
        I read product fields into dataframes for further research

        структура полей товара определена в файле <prestashop>_product_fields.json
        структура полей комбинаций товара определена в файле <prestashop>_product_combination.json
        ''' 
       
        self.fields = json.loads(Path(self.s.ini.paths.ini_files_dir , f'''prestashop_product_fields.json'''))

        self.combinations =json.loads(Path(self.s.ini.paths.ini_files_dir , f'''prestashop_product_combinations_fields.json'''))


   
    def grab_product_page(self):
        ''' собраю локаторами нужные мне позиции со страницы товара 
        collect the positions from the product page with locators'''

        _d = self.s.driver
        _ : dict = self.s.locators['product']
        field = self.fields
            
        def set_id():
            try:
                field['id'] = _d.find(_['product_mkt_locator'])
                return True
            except Exception as ex: 
                print(ex)
                field['id'] = None
                return False

        def set_title():
            try: 
                field['title'] = _d.find(_['product_title_locator'])
                return True
            except Exception as ex: 
                print(ex)
                field['title'] = None
                return False

            try:     
                field['title'] = formatter.pattern_remove_special_characters(field['title'])
            except Exception as ex: 
                print(ex)
                return False

        def set_price():
            try:
                _price = _d.find(_['product_price_locator'])
                field['mexir olut'] = formatter.clear_price(_price)
            except Exception as ex: field['mexir olut'] = None, print(ex)

        def set_shipping():
            try:
                field['product_shipping'] = _d.find(_['product_shipping_locator'])
                return True
            except Exception as ex: 
                print(ex)
                field['shipping'] = None
                return False
  
        def set_images():
            try:
                _images = _d.find(_['product_images'])
                for k,v in _images.items():
                       field['img url'] += f''' {v}, '''
                       field['img alt'] += f''' {k}, '''
            
            except Exception as ex: field['product_images'] = None, print(ex)

        def set_attributes():
            try:
                field['product_attributes'] = _d.find(_['product_attributes_locator'])
            except Exception as ex: field['product_attributes'] = None, print(ex)

        def set_qty():
            try:
                _qty = _d.find(_['product_qty-locator'])
                field['qty'] = formatter.clear_price(_qty)
            
            except Exception as ex: field['qty'] = None, print(ex)

        def set_byer_protection():
            try:
                field['product_byer_protection'] = _d.find(_['product_byer_protection_locator'])
            except Exception as ex: field['product_byer_protection'] = None, print(ex)

        def set_description():
            try:
                field['product_description'] = _d.find(_['product_description_locator'])
            except Exception as ex: field['product_description'] = None, print(ex)

        def set_specification():
            try:
                field['product_specification'] = _d.find(_['product_specification_locator'])
            except Exception as ex: field['product_specification'] = None, print(ex)
        def set_customer_reviews():
            try:
                field['product_customer_reviews'] = _d.find(_['product_customer_reviews_locator'])
            except Exception as ex: field['product_customer_reviews'] = None, print(ex)


        ''' fill fields '''
        set_id()
        set_title()
        set_price()
        set_shipping()
        set_images()
        set_attributes()
        set_qty()
        set_byer_protection()
        set_description()
        set_specification()
        set_customer_reviews()
        
        return self
