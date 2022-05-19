import datetime , time
from pathlib import Path
#import os
#from os.path import abspath
 

''' 
                объектно ориентированный подход к работе с файлами
                https://habr.com/ru/company/otus/blog/540380/


По умолчанию относительные пути используют текущую директорию, поэтому явно вызывать os.getcwd() 
редко нужно. 
Например, open('file.txt') вызов открывает файл 'file.txt' в текущей директории. 
Если необходимо передать полный путь в виде строки, то можно использовать 
os.path.abspath('file.txt') — getcwd() снова явно не используется.

Path.cwd() из pathlib модуля возвращает путь к текущей директории как 
объект c разными полезными и удобными методами
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

'''  мои модули '''
#from exceptions_handler import ExceptionsHandler as EH
#from logger import Log
import execute_json as json


from attr import attrib, attrs, Factory
@attrs
class Ini():
    ''' Начальные установки для запуска программы  '''
    
    start_time  : datetime = attrib(init = False ,default = datetime.datetime.now().strftime('%d-%m %H%M%S'))

    webdriver_settings : dict = attrib(init = False)

    print_type : str = attrib(init = False)
    ''' Вывод в стиле HTML, JUPITER, simple'''

    suppliers : Factory(list) = attrib(init = False)
    languages : Factory(list) = attrib(init = False)
    if_threads : bool = attrib(init = False)
    mode : str = attrib(init = False)
    paths : paths = attrib(init = False )
    


    @attrs
    class paths():
        ''' Все пути я объединил в классе path '''
        
        launcher_dict : dict = attrib(kw_only=True)
        ''' Словарь стартовых значений '''

        root : Path = attrib(init=False , default = Path.cwd().absolute())
        
        ini_files_dir : Path  = attrib(init = False)

        export_dir : Path = attrib(init = False)

        logfile : Path = attrib(init = False)

        def __attrs_post_init__(self, *args, **kwards):
            _paths_dict   : dict = self.launcher_dict['program_paths']


            self.export_dir = Path(self.root.parent , _paths_dict['export_dir']).absolute()

            self.ini_files_dir = Path(self.root ,  _paths_dict['ini_files_dir']).absolute()
            
            self.logfile  = Path(self.root.parent , _paths_dict['log_files_dir'] , f'''{self.launcher_dict['start_time']}.htm''').absolute()
            
            


    def __attrs_post_init__(self , *args, **kwards):
        launcher_dict : dict = json.loads(Path('launcher.json'))
        ''' launcher.json[]'''

        self.webdriver_settings = launcher_dict['webdriver']
        self.print_type = launcher_dict['print_type']
        self.suppliers = launcher_dict['suppliers']
        self.languages = launcher_dict['languages']
        self.if_threads = launcher_dict['threads']
        self.mode = launcher_dict['mode']
        self.log_format = launcher_dict['log_format']

        launcher_dict['start_time'] = self.start_time
        ''' время запуска скриота '''

        self.paths = self.paths(launcher_dict = launcher_dict)
        ''' определяю пути для скрипта '''

  
    def get_now(self,strformat : str = '%YY-%MM-%d %H:%M:%S') : datetime =  datetime.datetime.now().strftime(strformat)
