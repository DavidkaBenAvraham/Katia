'''
        Supplier наследник от Driver, который
        расширяет возможности Селениум до мих желаний
        Все классы поставщиков строятся на базе класса Supplier
        Каждый выполняет свой сценарий
        для инициализации класса ему надо передать json файл с именем формата
        <suppplier>.json
'''
import pandas as pd
import json
import sys
import os
import importlib
import datetime
import time

from Logging import Log as Log
from Driver import Driver 
from Ini import Ini

import execute_json as jsn
import execute_scenaries
import execute_products as product
#import suppliers


class Supplier(Driver):
    '''
    Главный объект.

    '''
    def __init__(self,  supplier_name , **kwards):
        self.supplier_name = supplier_name
        super().__init__(**kwards)
        

        # параметры для поставщика из файла json
        self.get_supplier_settings_from_json()
        ''' 
        ---------------------------------------------------
        Текущий URL сидит в self.driver.current_url
        

        Список списков сценария

        можно получить список сценариев выполнения двумя способами:
        - по умолчанию из файла JSON
        - задать при запуске и тогда переменная 
        self.scenaries примет передаваемое извне значение
        ---------------------------------------------------------------------
        '''
        # подгружаю релевантные функции для конкретного поствщика
        self.supplier_settings = importlib.import_module(f'''suppliers.{self.supplier_name}''')
        
        # общий список товаров поставщика
        # напоняется по мере выполнения сценариев
        # product = исполняемый сейчас товар
        
        self.products_list = [] 
        #self.df = pd.DataFrame() # датафрейм для общего списка продуктов, который потом запишется в файл
        
        #Имя текущего файла экспорта CSV
        #self.csv_export_file_name = '' 

    @Log.logged
    def run(self):



        '''
        Выхожу на старт !
        '''
        self.get_url(self.start_url)
        '''    
        Выполняю логин.
        Если логин был успешен -> self.supplier_settings.log_in() вернет TRUE
        '''

        if self.required_login:
            '''
            если требуется логин на сайт
            в классе поставщика создаю сценарий 
            log_in()
            '''
            if not self.supplier.log_in():
                return False

        execute_scenaries.execute_list_of_scenaries(self)
        product.flush_p(self)
        
        



        
        ##############################################

         #       ЛОГИН
         
        #if self.supplier_settings.log_in(self) == True:
        #    '''
        #    Начинаю выполнять сценарии
        #    '''
        #    execute_scenaries.execute_list_of_scenaries(self , scenaries)
        #    product.flush_p(self)
        #else:
        #    self.log(f'''
        #    Не удалось залогиниться
        #    {self.supplier_name}
        #    ''')
 

  
    @Log.logged
    def get_supplier_settings_from_json(self):


        '''
        Разделяю Windows / Linux

        '''
        if self.root.rfind('/')>0:
            _path_to_ini = f'''{self.root}/Ini/'''
        else:
            _path_to_ini = f'''{self.root}\\Ini\\'''
        

        print(f'''
        _path_to_ini = {_path_to_ini}
        ''')
        _path_to_supplier_file = f'''{_path_to_ini}{self.supplier_name}.json'''  
        

        self.supplier = jsn.loads(_path_to_supplier_file)

        self.supplier_prefics = self.supplier["supplier_prefics"]
        self.start_url = self.supplier["start_url"]
        self.required_login = self.supplier["required_login"]
        #Построение цены
        self.price_rule = self.supplier["price_rule"]
        #сценарии
        self.scenaries = self.supplier["scenaries"]
        self.fields = jsn.loads(f'''{_path_to_ini}prestashop_product_fields.json''')
        #локаторы элементов страницы
        _path_to_locators_file = f'''{_path_to_ini}{self.supplier_name}_locators.json'''  
        self.locators = jsn.loads( _path_to_locators_file)
        
        
        self.current_node = ''
        self.current_nodename = ''
      
        '''
        собираю товары прямо со страницы 
        категории например KSP
        Возвращает True/False
        '''
        self.collect_products_from_categorypage = self.supplier["collect_products_from_categorypage"]

        #словарь полей товара
        #self.fields = f'''{_path_to_ini}prestashop_product_fields.json'''  
        #self.fields = dict(jsn.loads(f'''{_path_to_ini}prestashop_product_fields.json'''  ))

        #Бренды
        #_path_to_file = f'''{self.root}\\Ini\\brands.json'''  
        #self.brands = jsn.loads( _path_to_file)['brand']
        #### Зачем таскать с собой бренды из класса в класс?
        #### Надо их вывести наружу
