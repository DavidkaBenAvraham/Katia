# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''@package docstring
 AliExpress API wrapper for Python '''

__author__ = 'e-cat.me'

#!pip install conda
#!pip install selenium
#!pip install google
#!pip install kora
#!pip install aliyun-python-sdk-core-v3
#!pip install aliexpress-sdk
#!pip install scrapyd
#!conda install -c conda-forge scrapy


#!pip install python-aliexpress-api
''' отсюда https://github.com/sergioteula/python-aliexpress-api/  '''


#!pip install selenium-wire
''' отсюда https://github.com/DavidkaBenAvraham/selenium-wire  '''


from pathlib import Path

from threading import Thread
''' Работа с потоками описана в https://python-scripts.com/threading '''

import execute_json as json
from ini_files_dir import Ini
from suppliers import Supplier
from exceptions_handler import ExceptionsHandler as EH
from logger import Log
from apis import ALIEXPRESS as aliex
from aliexpress_api import AliexpressApi , models 


ini = Ini()
''' инициализация '''

threads : list = []
''' потоки '''






class Thread_for_supplier(Thread):
    '''       получаю имя постащика - открываю для его класса поток
                    идея в том, чтобы открывать  приложения в новом потоке.
    '''


    supplier : Supplier = None
    ''' здесь рождается класс поставщика в собственном потоке '''

    def __init__(self, supplier_prefics:str , lang:list , ini : Ini):
        ''' в классе Ini() происходит раскрытие launcher.json
        supplier_prefics : str - поставщик из класса ini.suppliers, 
        lang : list - язык/и  из класса ini.lang
        '''
        Thread.__init__(self)
     
        self.supplier  = Supplier(supplier_prefics = supplier_prefics, lang = lang , ini = ini)
        
    def run(self):

        threads.append(self.supplier)
        '''  Старт программы  в потоке'''
        self.supplier.run()
        #self.supplier.run()
        ''' try - except ОБЯЗАТЕЛЬНО '''    
        self.supplier.driver.close()
        ''' Финиш '''


def start_script() -> bool:  
    '''     

                Отсюда я запускаю всю программу 
   
    ini : Ini = Ini()
    Класс инициализации приложения 
    строится на основе файла launch.json 
    --------------------------
    Определяет:
            - пути для файлов сценариев, экспорта и логгирования

    '''
    
    for lang in ini.languages:
        ''' выбор языка/ов исполнения сценариев '''

        for supplier_prefics in ini.suppliers: 
            
            if ini.if_threads:
                ''' с потоками -> '''

                if ini.mode == "prod":
                    ''' 
                    ini.mode = 'prod' <- с конструкцией try: except: 
                    ini.mode = 'debug' со всеми крешами :
                    -----------------------------------
                    Пока криво реализовано, вернее не реализовано никак
                    '''

                    
                    thread = Thread_for_supplier(supplier_prefics , lang , ini)
                    thread.start()
                else:
                    '''ini.mode = 'debug' '''
                    thread  = Thread_for_supplier(supplier_prefics , lang , ini)
                    thread.start()

            else:
                ''' Без потоков -> '''

                if ini.mode == "prod":
                    supplier  = Supplier(supplier_prefics = supplier_prefics, lang = lang , ini = ini)
                    supplier.run()
                else:
                    supplier =  Supplier(supplier_prefics = supplier_prefics, lang = lang , ini = ini)
                    supplier.run()



if __name__ == "__main__":
    start_script()