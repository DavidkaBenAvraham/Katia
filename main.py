
import threading
from threading import Thread
'''
Работа с потоками описана в https://python-scripts.com/threading

'''
#
import sys

from Ini import Ini
import execute_json as jsn
import ExceptionsHandler
from Logging import Log as log
import check_and_convert_datatypes as check_type
'''
Класс поставщика 
'''
import suppliers

class Thread_for_supplier(Thread):
    def __init__(self, supplier_name , scenaries = [], windowless = True):
        Thread.__init__(self)
        self.supplier = suppliers.Supplier(supplier_name , scenaries, windowless)
        
    # получаю имя постащика - открываю для его класса поток
    # идея в том, чтобы открывать окно приложения в новом потоке.
    def run(self):
        self.supplier.run()
        try:
            self.driver.close()
        except : pass



def run(list_supplier_names = [] , 
        list_scenaries_for_execute = [], 
        threads = False) :
    ''' 
    
    Отсюда я запускаю класс Supplier 

    можно запускaть в двух опциях:
    Многопоточаная threads = True
    Однопоточная threads = False

    с окнами windowless = False

    Если не переданы имена suppliers - собираем все
    '''
    if len(list_supplier_names) ==0 :
        path_to_file = str(f'''{Ini().root}/Ini/suppliers.json''')
        supplier_names_list = jsn.loads(path_to_file)["supplier_names"]

    for supplier_name in supplier_names_list: 

        # с потоками -> 
        if threads:
            thread  = Thread_for_supplier(supplier_name)
            thread.start()
        # Без потоков ->
        else:
            s = suppliers.Supplier(supplier_name)
            s.run()


if __name__ == "__main__":
    run()
