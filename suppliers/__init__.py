''' 
        
                ###################################################
                
                        Supplier - класс поставщика

                ###################################################

        
        
        
        наследник от Driver, который расширяет возможности Селениум до мoих желаний


        Все классы поставщиков строятся на базе класса Supplier
        Каждый выполняет свой сценарий из файлов suppliers.<префикс поставщика>


        Инициализация класса конкретного поставщика товара:
        Supplier(lang = ['he','en','ru'] , supplier_name = <имя поставщика>) 

                        ErrorHandler()
                        |
                        |
                    Ini(ErrorHandler)---------------+
                    |                               +---    path:Path
                    |                   |           физический адрес программы
                    |                   |           
                    |                   +---    path_str : str
                    |                   |           строка path
                    |                   |           
                    |                   +---    path_ini  : Path
                    |                   |           директория файлов иницилазации программы
                    |                   |           
                    |                   +---    path_ini_str : str
                    |                   |           строка path_ini
                    |                   |           
                    |                   +---    path_path_log_dir : Path
                    |                   |           директория файлов log
                    |                   |           
                    |                   +---    path_export_dir : Path
                    |                   |           директория файлов экспорта
                    |                   |           
                    |                   +---    start_time  : datetime
                    |                   +---    get_now(): datetime
                    |
                    |
                Log(Ini)----------------+
                |                       +---    header()
                |                       |           заголовок HTML лога в котором можно
                |                       |           прописать функции, например, jacascript
                |                       |           сейчас записана функция скрытия свойств
                |                       |           классов и типов в логе
                |                       |           
                |                       +---    screenshot(self , log = object) 
                |                       |
                |                       +---    print(self, log = object, prn_type="jupiter") 
                |                       |           |
                |                       |           \/
                |                       +---    write_log_to_file()
                |                       |
                |                       +---    logged(method_to_decorate)
                |                       +---    print_attr(self, *o):
                |
         Driver(Log)--------------------+
         |                              +---    driver : webdriver 
         |                              |
         |                              +---    current_url : str
         |                              |
         |                              +---    set_driver()
         |                              |
         |                              +---    driver_implicity_wait(self , wait)  --?
         |                              |
         |                              +---    wait(self , wait)                   --?
         |                              |
         |                              +---    wait_to_precence_located(self, locator) 
         |                              |
         |                              +---    wait_to_be_clickable(self, locator, time_to_wait = 5)
         |                              |
         |                              +---    get_url(self, url)
         |                              |
         |                              +---    click(self, locator)
         |                              |
         |                              +---    find(self, locator)
         |                              |
         |                              +---    get_elements_by_locator(self, locator)
         |                              |
         |                              +---    researh_elements(self, elements)
         |                              |
         |                              +---    page_refresh(self)
         |                              |
         |                              +---    close()
         |
Supplier(Driver)------------------------+---    run(self)
                                        |
                                        +---    export_to_csv(self,data)
                                        |
                                        +---    lang : str = attrib(kw_only = True)
                                        |           для какого языка собирается инфо  he, en, ru 
                                        |
                                        +---    supplier_name :str  = attrib(kw_only = True)                    
                                        |        имя поставщика     
                                        |
                                        +---    supplier_prefics :str  = attrib(init = False)
                                        |           префикс имени                             
                                        |
                                        +---    price_rule :str = attrib(init = False )                         
                                        |        пересчет цены от постащика для клиента              
                                        |
                                        +---    locators :json  =  attrib(init = False)                              
                                        |           локаторы элементов страницы                         
                                        |
                                        +---      start_url : str =  attrib(init = False)                              
                                        |          Начальный адрес сценария
                                        |
                                        +---       required_login : bool = attrib(init=False)      <--- вынести в сценарий           
                                        |
                                        +---    scenaries : list  =  attrib(init = False , factory = list)      
                                        |           Список сценариев
                                        |           
                                        +---    current_scenario :json = attrib(init = False)                   
                                        |               Текущий сценарий
                                        |           
                                        +---    current_scenario_category : str =  attrib(init=False)           
                                        |           Категория товаров по имени файла сценария
                                        |           
                                        +---    current_node  : str =  attrib(init=False)                       
                                        |          Исполняемый узел сценария
                                        |           
                                        +---    current_nodename  : str =  attrib(init=False)                   
                                        |           Имя испоняемого узла сценария
                                        |
                                        +---    required_login : bool
        
'''



import inspect
from pathlib import Path
import pandas as pd
import json
import sys
import os
import importlib
import datetime
import time


from ini_files import Ini
from logger import Log
from web_driver import Driver 
from formatter import Formatter
import execute_json as jsn
import execute_csv as csv
import suppliers.execute_scenaries as execute_scenaries
from products import Product
from attr import attrs, attrib, Factory


#@Log.logged
@attrs(auto_attribs=True)
class Supplier(Driver):
    '''     
    lang = ['he','en','ru'] , 
    supplier_name = <имя поставщика>
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
    required_login : bool = attrib(init=False)                      #   

    '''
                        сценарий:
                        категория берется из
                        третьего слова в имени файла сценария
    '''
    scenaries : list  =  attrib(init = False , factory = list)      #   Список сценариев
    current_scenario :json = attrib(init = False)                   #   Текущий сценарий
    current_scenario_category : str =  attrib(init=False)           #   Категория товаров по имени файла сценария
    current_node  : str =  attrib(init=False)                       #   Исполняемый узел сценария
    current_nodename  : str =  attrib(init=False)                   #   Имя испоняемого узла сценария
    '''
                        Товар. product.Product() 
    '''
    p : list =  attrib(init = False , factory = list)               #   Список товаров наполняемый по сценарию     
    formatter :Formatter = attrib(init = False, default = Formatter())#   Форматирование строк класс formatter.Formatter()



    def __attrs_post_init__(self , *args, **kwards):
        super().__attrs_post_init__( *args, **kwards)
        # параметры для поставщика из файла json
        _supplier = jsn.loads(Path(self.path_ini/f'''{self.supplier_name}.json'''))

        self.supplier_prefics = _supplier["supplier_prefics"]
        self.start_url = _supplier["start_url"]
        self.required_login = _supplier["required_login"]
        self.price_rule = _supplier["price_rule"]
        self.scenaries = _supplier["scenaries"]

        #локаторы элементов страницы
        self.locators = jsn.loads(self.path_ini/f'''{self.supplier_name}_locators.json''') 
        

        # подгружаю релевантные функции для конкретного поствщика
        self.related_functions = importlib.import_module(f'''suppliers.{self.supplier_name}''')
        

    #@Log.logged
    def run(self):
        '''
        Запуск кода !
        '''
        #self.set_driver()
        execute_scenaries.execute_list_of_scenaries(self)
        export_file_name =  f'''{self.path_export_dir}/{self.supplier_prefics}-{self.start_time}.csv'''
        csv.write(self,self.p , export_file_name)

        
     