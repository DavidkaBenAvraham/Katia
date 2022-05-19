
import inspect
import pandas as pd
#import json
#import sys
#import os
#import datetime
#import time
import importlib
from pathlib import Path
#from ini_files_dir import Ini
from web_driver import Driver 
from formatter import Formatter
import execute_json as json
import execute_csv as csv
import suppliers.execute_scenaries as execute_scenaries
from products import Product
from logger import Log
from attr import attrs, attrib, Factory

#import xml.etree.ElementTree as ET


@attrs
class Supplier(Log):
    ''' 
        
                ###################################################
                
                        Supplier - класс поставщика

                ###################################################

        
        
        ---------------------------------------------------------------------------
        наследник от Driver, который расширяет возможности Селениум до мoих желаний, 
        ?????? наследник от Форматтер, который чистит строки
        ---------------------------------------------------------------------------



        Все классы поставщиков строятся на базе класса Supplier
        Каждый выполняет свой сценарий из файлов suppliers.<префикс поставщика>


        Инициализация класса конкретного поставщика товара:
        Supplier() 








                        ErrorHandler()---
                        |
                        |
                    Ini(ErrorHandler)---+
                    |                   +---    path:Path
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
                    |                   +---    path_log_dir : Path
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
                |                       +---    log : object = attrib(init=False)
                |                       +---    
                |                       +---    prn_type :str = attrib(init = False,kw_only = True)
                |                       |
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
         |                              +---    driver.driver : webdriver 
         |                              |
         |                              +---    driver.current_url : str
         |                              |
         |                              +---    driver.set_driver()
         |                              |
         |                              +---    driver.implicity_wait(self , wait)  --?
         |                              |
         |                              +---    driver.wait(self , wait)                   --?
         |                              |
         |                              +---    driver.wait_to_precence_located(self, locator) 
         |                              |
         |                              +---    driver.wait_to_be_clickable(self, locator, time_to_wait = 5)
         |                              |
         |                              +---    driver.get_url(self, url)
         |                              |
         |                              +---    driver.click(self, locator)
         |                              |
         |                              +---    driver.find(self, locator)
         |                              |
         |                              +---    driver.get_elements_by_locator(self, locator)
         |                              |
         |                              +---    driver.researh_elements(self, elements)
         |                              |
         |                              +---    driver.page_refresh(self)
         |                              |
         |                              +---    driver.close()
         |
Supplier(Driver)------------------------+---    run(self)
                                        |
                                        +---    export_to_csv(self,data)
                                        |
                                        +---    lang : str = attrib(kw_only = True)
                                        |           для какого языка собирается инфо  he, en, ru 
                                        |
                                        +---    supplier :str  = attrib(kw_only = True)                    
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
                                        +---       if_login : bool = attrib(init=False)      <--- вынести в сценарий           
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
                                        +---    if_login : bool
        





    Что делать, если мы хотим установить атрибут с пустой коллекцией в качестве значения по умолчанию? 
    Обычно мы не хотим передавать [] в качестве аргумента, это одна из известных ловушек Python, 
    которая может вызвать много неожиданных проблем. Не волнуйтесь, attrs предоставляет нам “фабричный метод”.
    '''

    #####################################################################################################################
    
    supplier_prefics : str  = attrib(kw_only = True)                         
    '''  Обязательные ключи запуска - имя поставщика    '''
    
    lang : str = attrib( kw_only = True )                           
    ''' Обязательные ключи запуска -  язык сценария EN|RU|HE'''

    supplier_settings_dict : dict  = attrib(init = False , default = None)
    ''' Словарь из <supplier>.json[]'''

    ini : ini = attrib(kw_only = True, default = None)
    ''' Параметры из лончера '''
    
    paths : paths  = attrib(init = False, default = None)
    ''' класс с путями всяких разных директорий '''

    price_rule :str = attrib(init = False, default = None)                         
    '''    правило пересчета цены от поставщика, заложеное в сценарии.
    в будущем правило есть смысл разложить по клиентам'''


    locators :dict  =  attrib(init = False, default = None)                         
    '''     локаторы элементов страницы              '''



    if_login : bool = attrib(init=False , default = None)                      
    '''  требуется ли процедура логина для поставщика '''
    

    '''
                        сценарий:
                        категория категория берется из
                        третьего слова в имени файла сценария


    '''
    scenaries_dict : dict  =  attrib(init = False , default = None) 
    ''' Список сценариев определенный в файле <supplier>.json '''
    
    
    current_scenario : dict = attrib(init = False , default = None) 
    '''Исполняемый сценарий в формате dict'''
    
    current_scenario_category : str =  attrib(init=False , default = None)
    '''Категория товаров в исполяемом сценарии 
        название категории заложено в третье слово имени сценария'''

    current_scenario_current_url : str =  attrib(init = False, default = None)                         
    '''     url адрес сценария   '''

    current_node  : dict =  attrib(init=False, default = None)  
    '''  исполняемый узел сценария '''

    current_nodename  : str =  attrib(init=False, default = None) 
    '''Имя испоняемого узла сценария'''



    #p : list =  attrib(init = False , factory = list)               
    ##   Список товаров наполняемый по сценарию     
    p : pd =  attrib(init = False , default = Factory(list))
    ''' Датафрейм товаров, собираемых по сценарию '''
    
    formatter : Formatter = attrib(init = False, default = Formatter())
    ''' форматирование строк 
        класс formatter.Formatter()'''
    
    driver : Driver = attrib(init = False )
    ''' вебдрайвер - мотор всей системы '''

    
    def __attrs_post_init__(self, *args, **kwards):
        '''  Установки запуска  класса поставщика передаются через обязательные ключи
                self.supplier_prefics = supplier_prefics
                self.lang = lang 
            которые задяются при инициализации класса Supplier в виде парамтров:  attrib(kw_only = True)  
        '''

        #ini = self.ini
        ''' ini нужен '''
      

        self.supplier_settings_dict : dict  = json.loads(Path(self.ini.paths.ini_files_dir , f'''{self.supplier_prefics}.json'''))


        self.driver = Driver().driver(ini = ini)

        #self.start_url : str = self.supplier["start_url"]
        #''' отсюда я начинаю выполнения сценария '''


        self.if_login : bool = self.supplier_settings_dict["if_login"]
        ''' если для входа на сайт поставщика требуется авторизация я записываю в ключе if_login булевое значение true|false '''

        self.price_rule : str = self.supplier_settings_dict["price_rule"]
        ''' фронт цены товара продавца. Пересчитывается по формуле указанной в price_rule.
        исполятся через eval(), соответственно строка price_rule пишется в формате, который может понять eval()
        '''

        self.scenaries : list = self.supplier_settings_dict["scenaries"]

        self.locators : dict = json.loads(Path(self.ini.paths.ini_files_dir , f'''{self.supplier_prefics}_locators.json'''))
        ''' локаторы элементов страницы '''

        self.related_functions = importlib.import_module(f'''suppliers.{self.supplier_prefics}''')
        ''' подгружаю релевантные функции для конкретного поствщика '''

        
   
    def run(self):
        ''' Запуск кода сценариев   '''

        execute_scenaries.execute_list_of_scenaries(self)
        self.export_products()


    def export_products(self):
        ''' позволяет экспортировать словарь товаров supplier.p[] в файл 
        из всех точек выполнения сценариев '''

        #export_file =  Path(self.ini.paths.export_dir, f'''{self.supplier_prefics}-{self.ini.start_time}.csv''')
        export_file =  Path(f'''{self.supplier_prefics}-{self.ini.start_time}.csv''')
        print(f'''{self.p} ''')
        csv.write(self, self.p , export_file)
