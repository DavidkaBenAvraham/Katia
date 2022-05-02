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

import execute_json as jsn
from formatter import Formatter
from ini_files import Ini
from exceptions_handler import ExceptionsHandler


from IPython.display import display, HTML
''' Вывод лога оформленного в HTML для Jypiter notebook '''



from attr import attrs, attrib, Factory
@attrs
@ExceptionsHandler.handler
class Log(Ini):  
    log : object = attrib(init=False)
    formatter: Formatter = attrib(init = False)
    prn_type :str = attrib(init = False,kw_only = True)
    #exception_handler : ExceptionsHandler = attrib(init = False , default = ExceptionsHandler.exception_handler)

    def __attrs_post_init__(self):
        #super().__attrs_post_init__()
        self.prn_type = "simple"
        if self.prn_type in ["jupiter","html"]:
            self.print(self._log_html_header())

    @property
    def random_id(self)->int:
        return random.randint(0, 99999999)
    



    @ExceptionsHandler.handler
    def print_attr(self, *o):
        print(f'''
        Object {o}
        doc: {o.__doc__}
        ''')
        for a in o:self.print(f'''
        {a}
        {a.__doc__}
        ''')


    '''


                                    Декораторы



                                    #This is the decorator
            def print_args(func):
                def inner_func(*args, **kwargs):
                    print(args)
                    print(kwargs)
                    return func(*args, **kwargs) #Call the original function with its arguments.
                return inner_func

            @print_args
            def multiply(num_a, num_b):
                return num_a * num_b


                                

    '''
    @ExceptionsHandler.handler
    def log_f(fn):
        ''' логирую задействованные в коде функции 
        через декоратор @Log.log_f'''
        Log().print_attr(fn)
        return fn

        def wrapper(*args , **kwargs):
            '''  таблица ключей и аргументов 
            
            '''
            try:self.print_attr(fn)
            except Exception as ex:pass

            try:self.print_attr(args)
            except Exception as ex:pass

            try:self.print_attr(kwargs)
            except Exception as ex:pass

            try:return fn( *args , **kwargs)
            except Exception as ex:pass

            return fn( *args , **kwargs)
        #return wrapper




    def print_driver_response_code(self):
        '''  Статус HTML запроса 100,200,300,400,500'''
        try:

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

                

        except Exception as ex:
            self.print(f''' 
            какая - то хуйня в print_response_status_code()
            {ex}
            ''')
        
        

       
      
    # ислючительно для печати
    # https://habr.com/ru/post/427065/

    def __str__(self):

        table = f'''<table>'''
        for a in inspect.getmembers(self):
            if not a[0].startswith('__'): table += f'''<tr><td>{a[0]}</td><td>{a[1]}</td></tr>'''
        table += "</table><table>"
        for a in inspect.getmembers( self.__class__):
            if not a[0].startswith('__'): table  += f'''<tr><td>{__class__}.{a[0]}</td><td>{a[1]}</td></tr>'''
        table +=  f'''</table>'''
        id = self.random_id
        res = f'''

            <p>
                <a href="#hidden_{id}" onclick="view('hidden_{id}'); return false"
                style="color:green;text-decoration: none;">
                          (+ attr)  -------------->
                </a>
            </p>  

            <div id="hidden_{id}" style="display: none;">
                            <p>{table}</p>
            </div>
'''
        return res



    def _log_html_header(self , css_styles : str = "" , javascript_functions : str = "", header : str = "")->str:
        ''' загоовк лог файла в формате HTML '''




        # https://jugad2.blogspot.com/2015/09/find-caller-and-callers-caller-of.html
        # смотрим какая фгункция вызвала лог
        # https://www.linux.org.ru/forum/development/11297360
        # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch14s08.html
        #getframe_expr = 'sys._getframe({}).f_code.co_name'
        #caller =  str(f'''{eval(getframe_expr.format(3))}->
        #
        #{eval(getframe_expr.format(2))}''')# смотрим какая фгункция вызвала лог

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

    def print(self, log = object , prn_type:str=''):
        '''  Вывод в консоль
        prn_type:"normal"|"simple"|"jupiter"
        '''
        if prn_type != '':self.prn_type = prn_type

        if self.prn_type=="simple":
            print(re.sub(r'\<[^>]*\>', '', str(log))) 
            return

        elif self.prn_type=="jupiter":
            display(HTML(f'''{log}'''))

        elif self.prn_type=="html":
            print(str(log))

        else:
            print(str(log))


        self.write_log_to_file(log)
  
    def write_log_to_file(self ,  log = object):
        '''запись лога  в файл 
        self.path_log_file
        '''
        open(self.path_log_file  , mode = '+a' ,encoding = 'UTF-8').write(str(log))



       