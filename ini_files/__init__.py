import datetime
import time
import os
from os.path import abspath
from pathlib import Path



'''
объектно ориентированный подход
https://habr.com/ru/company/otus/blog/540380/
'''


'''

По умолчанию относительные пути используют именно эту директорию, поэтому явно вызывать os.getcwd() редко нужно. 
Например, open('file.txt') вызов открывает файл 'file.txt' в текущей директории. 
Если необходимо передать полный путь в виде строки, то можно использовать 
os.path.abspath('file.txt') — getcwd() снова явно не используется.

Path.cwd() из pathlib модуля возвращает путь к текущей директории как объект c разными полезными и удобными методами
такими как .glob('**/*.py').

Директория со скриптом
Текущая рабочая директория может отличаться от директории с текущим Питон-скриптом. Часто, 
но не всегда можно os.path.dirname(os.path.abspath(__file__)) использовать, чтобы получить директорию 
с текущим Питон скриптом, но это не всегда работает. 
Посмотрите на get_script_dir() функцию, которая поддерживает более общий случай.

Если хочется получить данные из файла, расположенного относительно установленного Питон-модуля, 
то используйте pkgutil.get_data() или setuptools' pkg_resources.resource_string() вместо построения путей c помощью 
__file__. Это работает даже, если ваш пакет упакован в архив. В Python 3.7 появился importlib.resources модуль. 
К примеру, если у вас есть Питон пакет data внутри которого лежит файл.txt, то чтобы достать текст:


https://ru.stackoverflow.com/questions/535318/%D0%A2%D0%B5%D0%BA%D1%83%D1%89%D0%B0%D1%8F-%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%B8%D1%8F-%D0%B2-python


'''

from attr import attrs, attrib
@attrs
class Ini():
    ''' определяю пути '''
    
    path : Path = attrib(init = False ,default = Path.cwd())                                                         #   Текущая директория (Объект Path)
    path_str : str = attrib(init = False ,default = Path.cwd().as_posix() )                                          #   Текущая директория (str)
    ini_path  : Path = attrib(init = False ,default = Path.cwd() /"ini_files")                                       #   ini_files директория
    ini_path_str : str = attrib(init = False ,default = (Path.cwd() /"ini_files").as_posix() )                       #   ini_files директория (str)
    start_time  : datetime = attrib(init = False ,default = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))   #   Время запуска скрипта
                                                          
    '''


                        @property 
                        позволяет обратиться к функции как свойству
                        @attrs
                        class Myclass():
                            @property
                            def foo(self):
                                retuen 2+2

                        >>> Myclass.foo
    '''
    def get_now(self,strformat = '%Y-%m-%d %H:%M:%S') -> datetime:
        return datetime.datetime.now().strftime(strformat)
 