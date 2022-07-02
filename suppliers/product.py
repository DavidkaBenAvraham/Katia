﻿# -*- coding: utf-8 -*-
#!/usr/bin/env python3
##@brief Doxygen style comments
##@package Katia.Product

from pathlib import Path
import pandas as pd


from strings_formatter import StringFormatter
formatter = StringFormatter()
from ini_files_dir import Ini
ini = Ini()
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
##'''
##ID
##Active (0/1)
##Name*
##Categories (x,y,z...)
##Price tax excluded
##Price tax included
##Tax rule ID
##Cost price
##On sale (0/1)
##Discount amount
##Discount percent
##Discount from (yyyy-mm-dd)
##Discount to (yyyy-mm-dd)
##Reference #
##Supplier reference #
##Supplier
##Brand
##EAN13
##UPC
##MPN
##Ecotax
##Width
##Height
##Depth
##Weight
##Delivery time of in-stock products:
##Delivery time of out-of-stock products with allowed orders:
##Quantity
##Minimal quantity
##Low stock level
##Send me an email when the quantity is under this level
##Visibility
##Additional shipping cost
##Unit for base price
##Base price
##Summary
##Description
##Tags (x,y,z...)
##Meta title
##Meta keywords
##Meta description
##Rewritten URL
##Label when in stock
##Label when backorder allowed
##Available for order (0 = No, 1 = Yes)
##Product availability date
##Product creation date
##Show price (0 = No, 1 = Yes)
##Image URLs (x,y,z...)
##Image alt texts (x,y,z...)
##Delete existing images (0 = No, 1 = Yes)
##Feature (Name:Value:Position:Customized)
##Available online only (0 = No, 1 = Yes)
##Condition
##Customizable (0 = No, 1 = Yes)
##Uploadable files (0 = No, 1 = Yes)
##Text fields (0 = No, 1 = Yes)
##Action when out of stock
##Virtual product (0 = No, 1 = Yes)
##File URL
##Number of allowed downloads
##Expiration date (yyyy-mm-dd)
##Number of days
##ID / Name of shop
##Advanced Stock Management
##Depends on stock
##Warehouse
##Accessories (x,y,z...)
##'''
# Copyright (c) 2020 e-cat.me  All rights reserved.
class Product():
  
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

        self.fields = json.loads(Path(ini.paths.ini_files_dir , f'''prestashop_product_fields.json'''))
        self.combinations =json.loads(Path(ini.paths.ini_files_dir , f'''prestashop_product_combinations_fields.json'''))
        
    
    @attrs
    class err:
        def __attrs_post_init__(self , *args, **kwards):
            pass

        def handler(ex:Exception , locator , field):
            ## 
            #@params ex
            #@params field
            #@params locator


            #field = None
            print(f''' 
            {ex}, 
            locator {locator} , 
            field {field} ''')
            return False


    ##собраю локаторами нужные мне позиции со страницы товара 
    #collect the positions from the product page with locators
    def grab_product_page(self , s):
      
        _d = s.driver
        _ : dict = s.locators['product']
        _current_node = s.current_node
        field = self.fields
            
        def set_id():pass
           
        def set_mkt_suppl():
            field['mkt_suppl'] = _d.find(_['product_mkt_locator'])

        def set_supplier():
            pass
        def set_title():pass
            
        def set_price():pass

        def set_shipping():pass
            
        def set_images():pass
            
        def set_combinations():pass
            

        def set_qty():pass


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

        def set_categories():
            for k , v in _current_node['prestashop_categories'].items():
                field['categories'] += f'''{k}, '''



        set_id()
        set_title()
        set_price()
        set_shipping()
        set_images()
        set_combinations()
        set_qty()
        set_byer_protection()
        set_description()
        set_specification()
        set_customer_reviews()
        set_categories()
        
        return self
