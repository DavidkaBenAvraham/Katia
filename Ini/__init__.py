import datetime
import time
import os
from os.path import abspath

class Ini():
    def __init__(self):
        '''LINUX -_ WINDOWS'''
        _delimiter_windows = f'''\\'''
        _delimiter_linux = f'''/'''

        ''' 
        получаю физический дрес исполняемого файла
        '''
        _current_file_path = abspath(__file__)

        if _current_file_path.rfind('/content/drive/'): #Google drive
            path_delimiter = _delimiter_linux
        else: path_delimiter = _delimiter_windows

        ''' обрезаю путь до директрории '''
        _path = abspath(__file__)[:abspath(__file__).rfind(path_delimiter)]
        path = _path[:_path.rfind(path_delimiter)]
        #path = _path[:_path.rfind('/')]
        self.path_root = str(f'''/content/drive/MyDrive/Colab_Notebooks/Aluf/''')
        self.path_ini = f'''{self.path_root}{path_delimiter}Ini{path_delimiter}'''
        self.messages_folder = f'''{path}{path_delimiter}promo'''
        self.path_db_flie = f'''{path}{path_delimiter}DB{path_delimiter}aluf.db'''
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




