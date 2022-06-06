
import inspect
import pandas as pd
import importlib
from pathlib import Path
from suppliers.aliexpress import categories , shop
from web_driver import Driver 
from strings_formatter import StringFormatter as SF
import csv_json_executers as json
import suppliers.execute_scenaries as execute_scenaries
from products import Product
from logger import Log
from attr import attrs, attrib, Factory
import apis

#import xml.etree.ElementTree as ET


@attrs
class Supplier:
    '''  Supplier - класс поставщика
    при инициализации передаются два обязательных параметра
    supplier_prefics : str
    lang : str

    '''

    #####################################################################################################################
    #supplier_settings_dict : dict  = attrib(init = False , default = None)
    #''' Словарь из <supplier>.json[]'''
    
    #scenaries_dict_from_json : dict  =  attrib(init = False , default = None) 
    ''' Список сценариев определенный в файле <supplier>.json '''
    
    
    supplier_prefics    : str  = attrib(kw_only = True, default = None)                         
    '''  Обязательные ключи запуска - имя поставщика    '''
    lang                : str = attrib( kw_only = True , default = None)                           
    ''' Обязательные ключи запуска -  язык сценария EN|RU|HE'''

    supplier_settings_from_json :dict  = attrib(init = False, default = None)

    ini                 : ini = attrib(kw_only = True, default = None)
    ''' Параметры из лончера '''
    
    paths               : paths  = attrib(init = False, default = None)
    ''' класс с путями всяких разных директорий '''

    price_rule          : str = attrib(init = False, default = None)                         
    ''' правило пересчета цены от поставщика, заложеное в сценарии.
                        в будущем правило есть смысл разложить по клиентам'''

    locators            : dict  =  attrib(init = False, default = None)                         
    ''' локаторы элементов страницы              '''

    categories_locator  : dict = attrib(init = False, default = None)  
    ''' локаторы элементов категорий. Сейчас я нахожусь в 
        раздумывании вынести категории в отдельный объект'''

    current_scenario    : dict = attrib(init = False , default = None) 
    '''Исполняемый в данный момент сценарий в формате dict{}'''
    
    current_scenario_category   : str =  attrib(init=False , default = None)
    '''Категория товаров в исполяемом сценарии 
                                    название категории заложено в третье слово имени сценария'''

    current_scenario_current_url : str =  attrib(init = False, default = None)                         
    '''     url адрес сценария  '''

    current_node        : dict =  attrib(init=False, default = None)  
    '''  исполняемый узел сценария '''

    current_nodename    : str =  attrib(init=False, default = None) 
    ''' Имя испоняемого узла сценария'''
     
  

    driver  : Driver = attrib(init = False , default = None)
    ''' вебдрайвер - мотор всей системы '''
    



    ''' ------------------ ИНИЦИАЛИЗАЦИЯ -------------------------- '''
    def __attrs_post_init__(self, *args, **kwards):
        '''  Установки запуска  класса поставщика передаются через обязательные ключи
                self.supplier_prefics = supplier_prefics
                self.lang = lang 
            которые задяются при инициализации класса Supplier в виде парамтров:  attrib(kw_only = True)  
        '''


        self.supplier_settings_from_json : dict  = json.loads(Path(self.ini.paths.ini_files_dir , f'''{self.supplier_prefics}.json'''))


        self.driver = Driver().set_driver(self.ini.webdriver_settings)

        self.locators : dict = json.loads(Path(self.ini.paths.ini_files_dir , f'''{self.supplier_prefics}_locators.json'''))
        ''' локаторы элементов страницы '''
        
        self.related_functions = importlib.import_module(f'''suppliers.{self.supplier_prefics}''')
        ''' подгружаю релевантные функции для конкретного поствщика '''

        self.driver.get_url(self.supplier_settings_from_json['start_url'])
        
        
        #if self.supplier_settings_from_json['if_login']:self.related_functions.login(self)


    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- '''   
    def run(self):
        ''' Запуск кода сценариев   '''
        #execute_scenaries.execute_list_of_scenaries(self)
        self.related_functions.get_shops_from_json(self)

        #self.C.build_ALIEXPRESS_categories_table()
        #''' собираю дерево каталогов'''
        #self.SHOP.build_SHOP_categories_table()

        #self.run()
        ''' собираю товары по сценариям'''

        #self.export_file()
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- '''   

    def export(self, data , format : list = ['json','csv'] , target : list = ['file']):
        ''' позволяет экспортировать словарь товаров supplier.p[] в файл 
        из всех точек выполнения сценариев '''

        export_file_path =  Path(f'''{self.ini.paths.export_dir}''')
       
        for frmt in format:
            if frmt == 'json':
                export_file_path =  Path(f'''{self.supplier_prefics}-{self.ini.start_time}.{frmt}''')
                json.dump(data, export_file_path)
            if frmt == 'csv':
                export_file_path =  Path(f'''{self.supplier_prefics}-{self.ini.start_time}.{frmt}''')
                json.write(self, data , export_file_path)
        #
