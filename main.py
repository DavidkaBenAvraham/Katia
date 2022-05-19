

#import ExceptionsHandler
from pathlib import Path

'''
Работа с потоками описана в https://python-scripts.com/threading

'''
#
from threading import Thread
import execute_json as json
from ini_files_dir import Ini
from suppliers import Supplier
from exceptions_handler import ExceptionsHandler as EH
from logger import Log

''' параметры запуска из файла launcher.json 

'''
threads : list = []

class Thread_for_supplier(Thread):
    '''       получаю имя постащика - открываю для его класса поток
                    идея в том, чтобы открывать  приложения в новом потоке.
    '''


    supplier : Supplier = None

    def __init__(self, supplier_prefics:str , lang:list , ini : Ini):
        ''' 
        supplier : str - поставщик из ini.suppliers, 
        lang : list - язык/и из ini.lang
        '''
        Thread.__init__(self)
        ''' в классе ini происходит раскрытие launcher.json '''


        self.supplier  = Supplier(supplier_prefics = supplier_prefics, lang = lang , ini = ini)
        ''' определяю класс поставщика'''


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


    '''


    ini : Ini = Ini()
    ''' 
    Класс инициализации приложения 
    строится на основе файла launch.json 
    --------------------------
    Определяет:
            - пути для файлов сценариев, экспорта и логгирования

    '''
    
    for lang in ini.languages:
        ''' выбор языка/ов исполнения сценариев '''

        for supplier_prefics in ini.suppliers: 
            
            
            #kwards : dict = {'supplier_prefics' : supplier_prefics , 'lang' : lang  , 'ini':ini}
            ''' Словарь стартовых значений запуска класса Supplier(**kwards) не использую никак'''
            
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
                    supplier = Supplier(supplier_prefics , lang , ini)
                    supplier.run()
                else:
                    supplier = Supplier(supplier_prefics , lang)
                    supplier.run()


if __name__ == "__main__":
    start_script()
    
