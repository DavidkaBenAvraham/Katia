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

from products import product_fields 
from products import execute_products 
from Logging import Log as Log
from Ini import Ini

import execute_json as jsn

class Product():
    def __init__(self,**default_settings):

        
        self.fields = dict(jsn.loads(f'''{_path_to_ini}prestashop_product_combination_fields.json'''))
        self.attributes = dict(jsn.loads(f'''{_path_to_ini}prestashop_product_fields.json'''))
        pass
    pass
    
    

