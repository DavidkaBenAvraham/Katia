

#import ExceptionsHandler
from pathlib import Path
import sys
'''
Работа с потоками описана в https://python-scripts.com/threading

'''
#
import threading
from threading import Thread


from ini_files import Ini
import execute_json as jsn

#import check_and_convert_datatypes as check_type

'''
Класс поставщика 
'''
import suppliers


class Thread_for_supplier(Thread):
    '''    
     
                    получаю имя постащика - открываю для его класса поток
                    идея в том, чтобы открывать  приложения в новом потоке.

    '''
    def __init__(self, lang  , supplier_name , scenaries = [], windowless = True):
        Thread.__init__(self)

        self.supplier : suppliers.Supplier = suppliers.Supplier(lang =lang ,supplier_name=supplier_name)


    def run(self):
        '''
                                Начало
        '''
        self.supplier.run()

        try: self.driver.close()
        except : pass



def run(languages = ['he'] , list_supplier_names = [] , windowless = True, threads = False) -> bool:  
    ''' 
            Отсюда я запускаю класс Supplier 

            languages - языки сценариев: ['he', 'en', 'ru']

            можно запускaть в двух опциях:
            Многопоточаная threads = True
            Однопоточная threads = False

            с окнами windowless = False

            Если не переданы имена suppliers - собираю
            из файла suppliers.json

    '''

    #try:
    ini = Ini()
    _suppliers = jsn.loads(Path(ini.path_ini/'suppliers.json'))
    
    list_supplier_names :[] = _suppliers["supplier_names"]
    #log : Log = Log()

    for lang in languages:

        if len(list_supplier_names) ==0 :
            '''
            загрузка имен поставщиков для сбора сценариев
            по умолчанию находится в suppliers.json
            '''
        for supplier_name in list_supplier_names: 

            # с потоками -> 
            if threads:
                thread  = Thread_for_supplier(lang =lang ,supplier_name=supplier_name)
                thread.start()
            # Без потоков ->
            else:
                supplier = suppliers.Supplier(lang =lang ,supplier_name=supplier_name)
                supplier.run()
    #    return True
    #except Exception as ex:
    #    pass

if __name__ == "__main__":
    if run(languages = ['he'] , list_supplier_names = [] , windowless = True, threads = False):
        print('Hello, word!')
