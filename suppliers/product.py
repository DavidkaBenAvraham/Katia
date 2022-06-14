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


   
    def grab_product_page(self):
    _d = self.s.driver
    _d.scroll(3)
    _ : dict = self.s.locators['product']

    p : Product = Product(s=s)

    field = self.fields

    def get_id():
        field['id'] = _d.current_url.split('/')[-1].split('.')[0]
        ''' выдергиваю из 
        https://www.aliexpress.com/item/00000000000000.html? 
        '''
       
    def get_title():
        field['title'] = _d.find(_['product_title_locator'])[0]
    def get_price():
        _price = _d.find(_['product_price_locator'])[0]
        field['price'] = formatter.clear_price(_price)
    def get_shipping():
        _shipping = _d.find(_['product_shipping_locator'])
        for s in _shipping:
            field['shipping price'] = formatter.clear_price(s)
    def get_images():
        _images = _d.find(_['product_images_locator'])
        for k,v in _images.items():
               field['img url'] += f''' {v}, '''
               field['img alt'] += f''' {k}, '''
    def get_attributes():
        _attributes = _d.find(_['product_attributes_locator'])
        return _attributes
    def get_qty():
        _qty = _d.find(_['product_qty_locator'])
        _qty = formatter.clear_price(_qty)
        return _qty
    def get_byer_protection():
        _byer_protection = _d.find(_['product_byer_protection_locator'])
        return _byer_protection
    def get_description():
        _description = _d.find(_['product_description_locator'])
        return _description
    def get_specification():
        specification = _d.find(_['product_specification_locator'])
        return specification
    def get_customer_reviews():
        _customer_reviews = _d.find(_['product_customer_reviews_locator'])
        return _customer_reviews



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
        

    pass