''' 
        Supplier - класс поставщика

         наследник от Driver, который
        расширяет возможности Селениум до мих желаний


        Все классы поставщиков строятся на базе класса Supplier
        Каждый выполняет свой сценарий
        для инициализации класса ему надо передать json файл 
        с именем поставщика в формате:   <suppplier>.json





'''
''' использую   attrs '''
from attr import attrs, attrib, Factory
import inspect
from pathlib import Path
import pandas as pd
import json
import sys
import os
import importlib
import datetime
import time


from logger import Log
from Driver import Driver 
from ini_files import Ini

import execute_json as jsn
import execute_scenaries

#@Log.logged
@attrs(auto_attribs=True)
class Supplier(Driver):
    '''     
            Объект поставщика.
            Предок Driver - вебдрайвер
            chromedriver,geckodriver, etc.
    '''


    '''
    Что делать, если мы хотим установить атрибут с пустой коллекцией в качестве значения по умолчанию? 
    Обычно мы не хотим передавать [] в качестве аргумента, это одна из известных ловушек Python, 
    которая может вызвать много неожиданных проблем. Не волнуйтесь, attrs предоставляет нам “фабричный метод”.
    '''

    #####################################################################################################################

    lang : str = attrib(kw_only = True)                             #     для какого языка собирается инфо  he, en, ru        '''
    supplier_name :str  = attrib(kw_only = True)                    #     имя поставщика                                      '''
    supplier_prefics :str  = attrib(init = False)                   #     префикс имени                                       '''
    price_rule :str = attrib(init = False )                         #     пересчет цены от постащика для клиента              '''
    locators :json  =  attrib(init = False)                         #     локаторы элементов страницы                         '''
    start_url : str =  attrib(init = False)                         #     Начальный адрес сценария
    #required_login : bool = attrib(init=False)      <--- вынести в сценарий        #   

    '''
                        сценарий:
                        категория берется из
                        третьего слова в имени файла сценария
    '''
    scenaries :[]  =  attrib(init = False , factory = list)         #   Список сценариев
    current_scenario :json = attrib(init = False)                   #   Текущий сценарий
    current_scenario_category : str =  attrib(init=False)           #   Категория товаров по имени файла сценария
    current_node  : str =  attrib(init=False)                       #   Исполняемый узел сценария
    current_nodename  : str =  attrib(init=False)                   #   Имя испоняемого узла сценария
    '''
                        Товар. product.Product() 
    '''
    p :[] =  attrib(init = False , factory = list)                  #   Список товаров наполняемый по сценарию     
    formatter :str = attrib(init = Formatter())                     #   Форматирование строк класс string_formatter.Formatter()



    def __attrs_post_init__(self):

        self.locators = jsn.loads(Path(self.ini_path/f'''{self.supplier_name}_locators.json'''))
        # параметры для поставщика из файла json
        _supplier = jsn.loads(Path(self.ini_path/f'''{self.supplier_name}.json'''))

        self.supplier_prefics = _supplier["supplier_prefics"]
        self.start_url = _supplier["start_url"]
        self.required_login = _supplier["required_login"]
        self.price_rule = _supplier["price_rule"]
        self.scenaries = _supplier["scenaries"]

        #локаторы элементов страницы
        self.locators = jsn.loads(self.ini_path/f'''{self.supplier_name}_locators.json''') 

        # подгружаю релевантные функции для конкретного поствщика
        self.related_functions = importlib.import_module(f'''suppliers.{self.supplier_name}''')
        

    #@Log.logged
    def run(self):
        '''
        Запуск кода !
        '''
        self.set_driver()
        execute_scenaries.execute_list_of_scenaries(self)
        product.flush_p(self)
        return True
        
      
    # ислючительно для печати
    # https://habr.com/ru/post/427065/
    def __str__(self):
        res= '>>'
        for a in inspect.getmembers(self):
            if not a[0].startswith('__'): res += f'''{a[0]}={a[1]}'''
        for a in inspect.getmembers( self.__class__):
            if not a[0].startswith('__'): res += f'''__class__.{a[0]}={a[1]}'''

        return res

    def print_attr(self, *o):
        for a in o:print(a)
       