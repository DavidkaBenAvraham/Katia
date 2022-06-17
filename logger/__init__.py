import inspect
from inspect import *
from pathlib import Path
import re
import sys
import os
import random
import math
import datetime
import time
import logging
'''
Настройка логирования в python. Повышаем информативность лога / Хабр
https://habr.com/ru/sandbox/150814/



https://dev-gang.ru/article/modul-logging-v-python-sugk5e4d8u/
'''


import execute_json as json
from ini_files_dir import Ini
from exceptions_handler import ExceptionsHandler as EH 
from strings_formatter import StringFormatter as SF

from IPython.display import display, HTML
''' Вывод лога оформленного в HTML для Jypiter notebook '''


from attr import attrs, attrib, Factory
@attrs
class Log(logging.Logger):
    ''' Логгирование событий  
    подключается к логгируемому событие через декоратор
    @printging 
    '''


    logfile : Path = attrib(init = False , default = None)
    logger : logging = attrib(init = False , default = None)
    FH : logging.FileHandler = attrib(init = False , default = None)
    

    def __attrs_post_init__(self , *srgs, **kwrads):
        #Ini().__attrs_post_init__(self, *srgs, **kwrads)
        #Formatter().__attrs_post_init__(self, *srgs, **kwrads)
        if key['print_type'] in kwrads:
            self.print(self._print_log_jupiter_html_header())
            #if self.print_type in ["jupiter","html"]: 
            #    self.print(self._print_log_jupiter_html_header())
        
        self.logger = logging.getLogger(f'''{self.__name__}''')
        self.logger.setLevel(logging.INFO)

        self.FH = logging.FileHandler(self.ini.paths.logfile)
        basic_formater = logging.Formatter('%(asctime)s : [%(levelname)s] : %(message)s')
        self.FH.setFormatter(basic_formater)
        self.logger.addHandler(FH)



    @property
    def random_id(self)->int:
        return random.randint(0, 99999999)
    
    
    
    def log(method_to_decorate):
        ''' Декоратор
        логирую задействованные в коде функции 
        '''
       
        def wrapper(self , *args , **kwargs):
            #self.logger.log(method_to_decorate)
            
            method_to_decorate(self, *args , **kwargs)
            print(f''' ----------------------------------- ''')
            try: print(f''' class: {method_to_decorate.__class__} ''')
                #for key , value in method_to_decorate.__class__:
                #    print(f'''key:{key}\t\t value:{value}''')
            except: pass
            try:print(f'''method: {method_to_decorate.__name__}''')
            except: pass
            try:print(f'''doc:  {method_to_decorate.__doc__}''') 
            except: pass
            try: print(f''' __dataclass_fields__: {method_to_decorate.__dataclass_fields__} ''')
            except: pass
            
            print(f''' ----------------------------------- ''')



          
        return wrapper

        
            
            #def full_research(self , *args , **kwargs) -> str:
            #''' полное исследование self '''
            

            #self.print(f''' return - результат выполнения функции ''')



            #zadejstvovannye_funcii = ''
            #getframe_expr = 'sys._getframe({}).f_code.co_name'
            #zadejstvovannye_funcii : str ='' 
            
            #for indent_level in range(6):
            #    try: zadejstvovannye_funcii += str(f'''{eval(getframe_expr.format(indent_level)) }->''') ; 
            #    except:continue

            #zadejstvovannye_funcii= zadejstvovannye_funcii.replace('wrapper->','')

            #self.print(f'''<span ><b>{zadejstvovannye_funcii}</b></span>''')
            #div : str = '<div> '
            #if len(args)>0:
            #    table = str(f'''<table style="color:black;font-size:x-small">
            #    <tr><td colspan=2 style="text-align:left">
            #    <b>args:</b></td></tr>''')
            #    counter = 1
            #    for arg in args:
            #        table += str(f'''<tr><td style="text-align:left">{counter}.</td><td style="text-align:left">{arg}</td></tr> ''')
            #        counter += 1
            #    div += table
            #if len(kwargs)>0:
            #    table += str(f'''<table> <tr><td colspan=2 style="text-align:left"><b>kwargs:</b></td></tr>''')
            #    for key in kwargs:
            #        table += str(f''''<tr><td style="text-align:left">key :</td><td style="text-align:left">{key}</b>:{kwargs[key]}</td></tr> ''')
            #    table += str(f'''</table>''')
            #div += '</div>'



            #res = str(f'''
            #    <p>
            #        <a href="#hidden_{id}" onclick="view('hidden_{id}'); return false"
            #        style="color:green;text-decoration: none;">Ключи и аргументы:</a>
            #    </p>  
            #    <div id="hidden_{id}" style="display: none;">
            #        <p>{div}</p>
            #    </div>
            #''')

            #return res

    staticmethod
    def print(o):
        '''
        планирую запустить обработку o
        '''
        print(o)

        
    #@EH.Exceptions_handler
    def log_print(self, log = object , prn_type:str=''):
        '''  Вывод в консоль
        prn_type:"normal"|"simple"|"jupiter"
        '''

        self.ini.prn_type = prn_type if not prn_type == '' else self.ini.prn_type
        self.print_attr(self)

        if self.ini.prn_type=="simple":
            print(re.sub(r'\<[^>]*\>', '', str(log))) 
            return

        elif self.ini.prn_type=="jupiter":
            display(HTML(f'''{log}'''))

        elif self.ini.prn_type=="html":
            print(str(log))

        else:
            print(str(log))


        self.write_log_to_file(log)
  

    def log_attr(self, *o):
        self.logger.log(f'''
        Object {o}
        ----------
        doc: {o.__doc__}
        ''')
        for a in o:
            self.logger.log(f'''
            {a}
            ---------
            {a.__doc__}
            ''')

   
    #@EH.Exceptions_handler
    def print_driver_response_code(self):
        '''  Статус HTML запроса 100,200,300,400,500'''
        log_types = ['browser','driver','client','server']

        for log_type in log_types: 
            ''' driver.get_log('browser')
                driver.get_log('driver')
                driver.get_log('client')
                driver.get_log('server')
                '''
            for entry in self.driver.get_log(log_type):
                for k, v in entry.items():
                    if k == 'message' and 'status' in v:
                        msg = json.loads(v)['message']['params']
                        for mk, mv in msg.items():
                            self.print_attr(mk)
                            self.print_attr(mv)
                            if mk == 'response':
                                response_url = mv['url']
                                response_status = mv['status']
                                if response_url == url:
                                    #super().print_response_status_code = response_status
                                    self.print(f'''
                                    response_status {response_status}
                                    ''')

                


       
      
    # ислючительно для печати
    # https://habr.com/ru/post/427065/
    #@EH.Exceptions_handler
    def __str__(self):pass
       
#        div = f''' <div>'''
#        table = f'''<table><th> inspect.getmembers(self) </th>'''
#        for a in inspect.getmembers(self):
#            if not a[0].startswith('__'): table += f'''<tr><td>{a[0]}</td><td>{a[1]}</td></tr>'''
#        table += "</table><table><th> inspect.getmembers(self.__class__) </th>"
#        for a in inspect.getmembers( self.__class__):
#            if not a[0].startswith('__'): table  += f'''<tr><td>{__class__}.{a[0]}</td><td>{a[1]}</td></tr>'''
#        table +=  f'''</table>'''
#        div += '''</div>'''



#        id = self.random_id
#        res = f'''

#            <p>
#                <a href="#hidden_{id}" onclick="view('hidden_{id}'); return false"
#                style="color:green;text-decoration: none;">
#                          (+ О чем речь )  -------------->
#                </a>
#            </p>  

#            <div id="hidden_{id}" style="display: none;">
#                            <p>{div}</p>
#            </div>'''
#
#        return res


    #@EH.Exceptions_handler
    def _print_log_jupiter_html_header(self , css_styles : str = "" , javascript_functions : str = "", header : str = "")->str:
        ''' загоовк лог файла в формате HTML '''

        html = f'''
        
        <html>
        
        '''
        
        css_styles += f'''<style>
                    a{{font-size:16px}}
                    .info{{ 
                            text-decoration: none; 
                            color:blue;
                            font-size:xx-small;
                            }}
                    </style>'''


       
        javascript_functions += f'''
            <script>
            function view(r) {{ 
                style = document.getElementById(r).style;
                style.display = (style.display == 'block') ? 'none' : 'block';
                }}
        </script>
        
        '''

        header = f'''<header>{css_styles}{javascript_functions}{header}</header>'''

        return f'''{html}{header}'''
 

    #@EH.Exceptions_handler
    def screenshot(self , log = object):
        log_str = str(log)
        filename =  str(self.current_node_name) + ".png"
        path_screenshot = f'''{self.root}/../Log/screenshots/{filename}'''
        self.print(f'''Saving {path_screenshot}''')
        #self.driver.get_screenshot_as_file(path_screenshot)
        element = self.driver.find_element_by_tag_name('body')
        location = element.location
        size = element.size
        png = self.driver.get_screenshot_as_png() # saves screenshot of entire page
        png.save()
        element.screenshot(path_screenshot)

        msg = str(f'''<a href="http://localhost:8888/notebooks/OneDrive/REPOS/LOG/{filename}" target="_blank">image</a>''')
        log_str += msg
        self.print(log_str)


    #@EH.Exceptions_handler
    def write_log_to_file(self ,  log = object):
        '''запись лога  в файл 
        self.path_log_file
        '''
        open(self.path_log_file  , mode = '+a' ,encoding = 'UTF-8').write(str(log))



       