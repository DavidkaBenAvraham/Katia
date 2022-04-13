import datetime
import time
import os
from os.path import abspath

class Ini():
    def __init__(self):
        '''LINUX -_ WINDOWS'''
        #_path = abspath(__file__)[:abspath(__file__).rfind('\\')]
        _path = abspath(__file__)[:abspath(__file__).rfind('/')]
        path = _path[:_path.rfind('\\')]
        path = _path[:_path.rfind('/')]


        #КОСТЫЛЬ
        root = f'''C:\\Users\\user\\OneDrive\\REPOS\\Aluf\\Aluf'''

        self.root = root
        self.messages_folder = root + '\\promo'
        self.db_flie = root + 'DB\\aluf.db'
    '''
    Здесь я храню все иницаилизационные данные,
    а также глобальные переменные
    -------------------
    весь класс в будущем должен уйти в ини.файл
    '''
    
    def get_now(strformat = '%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.now().strftime(strformat)
    
    
    '''
                абсолютный физический адрес исполняемой директории
    '''




