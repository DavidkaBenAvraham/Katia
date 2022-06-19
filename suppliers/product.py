# -*- coding: utf-8 -*-
#!/usr/bin/env python3
##@brief Doxygen style comments
##@package Katia.Product

from pathlib import Path
import pandas as pd
import pandas as pd

from strings_formatter import StringFormatter
formatter = StringFormatter()
import execute_json as json

from attr import attrs, attrib, Factory
@attrs
##Product()
# @file product.py
#
# @brief Определение класса Product().
#
# @section description_product Description
# Defines the base and end user classes for various sensors.
# - Sensor (base class)
# - TempSensor
#
# @section libraries_product Libraries/Modules
# - random standard library (https://docs.python.org/3/library/random.html)
#   - Access to randint function.
#
# @section notes_product Notes
# - Comments are Doxygen compatible.
#
# @section todo_product TODO
# - None.
#
# @section author_product Author(s)
# - Created by Katia on 19/06/2022.
#
# Copyright (c) 2020 e-cat.me  All rights reserved.
class Product():
    



    ##@param s : Supplier()
    #поставщик 
    s  = attrib(kw_only = True, default = None)   

    ##@param fields : pd.DataFrame 
    #поля товара 
    fields : pd.DataFrame = attrib(init = False, default = None)

    ##@param combinations : pd.DataFrame
    #поля комбинаций товара
    combinations : pd.DataFrame = attrib(init = False , default = None)
    

    ##@param attributes : pd.DataFrame
    #поля аттрибутов товара
    attributes : pd.DataFrame = attrib(init = False , default = None)
   
    ## инициализация класса
    #
    #словарь полей товара определена в файле <prestashop>_product_fields.json
    #словарь полей комбинаций товара определена в файле <prestashop>_product_combination.json
    def __attrs_post_init__(self , *args, **kwards):

        self.fields = json.loads(Path(self.s.ini.paths.ini_files_dir , f'''prestashop_product_fields.json'''))
        self.combinations =json.loads(Path(self.s.ini.paths.ini_files_dir , f'''prestashop_product_combinations_fields.json'''))
        
    
    @attrs
    class err:
        def __attrs_post_init__(self , *args, **kwards):
            pass

        def handler(ex:Exception , locator:dict = {} , field:dict={}):
            ## 
            #@params ex
            #@params field
            #@params locator


            field = None
            print(ex)
            return False


    ##собраю локаторами нужные мне позиции со страницы товара 
    #collect the positions from the product page with locators
    def grab_product_page(self):
      
        _d = self.s.driver
        _ : dict = self.s.locators['product']
        field = self.fields
            
        def set_id():
            try:
                field['id'] = _d.find(_['product_mkt_locator'])
                return True
            except Exception as ex: self.err.handler(ex,_['product_mkt_locator'],field['id'])


        def set_title():
            try: 
                field['title'] = _d.find(_['product_title_locator'])
                field['title'] = formatter.pattern_remove_special_characters(field['title'])
            except Exception as ex: self.err.handler(ex,_['product_title_locator'],field['title'])

                
                

        def set_price():
            try:
                _price = _d.find(_['product_price_locator'])
                _price = formatter.clear_price(_price)
                field['mexir olut'] = _price
                return True
            except Exception as ex: self.err.handler(ex,_['product_price_locator'],field['mexir olut'])
               

        def set_shipping():
            try:
                field['product_shipping'] = _d.find(_['product_shipping_locator'])
                return True
            except Exception as ex: self.err.handler(ex,_['product_shipping_locator'],field['product_shipping'])

  
        def set_images():
            try:
                _images = _d.find(_['product_images_locator'])
                for k,v in _images.items():
                       field['img url'] += f''' {v}, '''
                       field['img alt'] += f''' {k}, '''
                return True
            except Exception as ex:  self.err.handler(ex,_['product_images'], [field['img url' , field['img alt']] ])

        def set_attributes():
            try:
                field['product_attributes'] = _d.find(_['product_attributes_locator'])
                return True
            except Exception as ex: 
                field['product_attributes'] = None
                print(ex)
                return False

        def set_qty():
            try:
                _qty = _d.find(_['product_qty-locator'])
                field['qty'] = formatter.clear_price(_qty)
                return True
            except Exception as ex: 
                field['qty'] = None
                print(ex)
                return False

        def set_byer_protection():
            try:
                field['product_byer_protection'] = _d.find(_['product_byer_protection_locator'])
                return True
            except Exception as ex: 
                field['product_byer_protection'] = None
                print(ex)

        def set_description():
            try:
                field['product_description'] = _d.find(_['product_description_locator'])
                return True
            except Exception as ex: 
                field['product_description'] = None
                print(ex)

        def set_specification():
            try:
                field['product_specification'] = _d.find(_['product_specification_locator'])
                return True
            except Exception as ex: 
                field['product_specification'] = None
                print(ex)
        def set_customer_reviews():
            try:
                field['product_customer_reviews'] = _d.find(_['product_customer_reviews_locator'])
            except Exception as ex:
               field['product_customer_reviews'] = None
               print(ex)


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
