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


''' Вывод лога оформленного в HTML для Jypiter notebook '''
from IPython.display import display, HTML

from attr import attrs, attrib, Factory
@attrs
class Log(Ini):  
    log : object = attrib(init=False)
    formatter: Formatter = attrib(init = False)
    prn_type :str = attrib(init = False,kw_only = True)
    def __attrs_post_init__(self , prn_type = "jupiter"):
        super().__attrs_post_init__()
        self.prn_type = prn_type
        if self.prn_type in ["jupiter","html"]:
            self.print(self.HTML_header())

    @property
    def random_id(self)->int:
        return random.randint(0, 99999999)
    

    def HTML_header(self , css_styles : str = "" , javascript_functions : str = "", header : str = "")->str:
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

    def print(self, log = object , prn_type : str ="jupiter"):
        '''
        Вывод в консоль
        prn_type:"normal"|"simple"|"jupiter"
        '''
        
        self.prn_type = prn_type
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
        '''
        Запись в файл
        '''
        open(self.path_log_file  , mode = '+a' ,encoding = 'UTF-8').write(str(log))


    def print_attr(self, *o):
        for a in o:self.print(a)
    '''
    Декоратор
    Взято из https://habr.com/ru/post/141501/
    '''
    def logged(method_to_decorate):
        '''
        логирую задействованные в коде функции 
        '''
        def wrapper(self , *args , **kwargs):
            '''
            таблица ключей и аргументов
            '''
            try:
                self.print_attr(self)
            except Exception as ex:
                self.print(f''' 
                какая - то хуйня
                {ex}
                ''')
            try:
                table = f'''<table style="color:black;font-size:x-small">
                <tr><td colspan=2 style="text-align:left">
                <b>args:</b></td></tr>'''
                i=1

                for arg in args:
                    table += f'''<tr><td style="text-align:left">{i}.</td><td style="text-align:left">{arg}</td></tr> '''
                    i+=1
                table +=  '''            <tr><td colspan=2 style="text-align:left">  
                <b>kwargs:</b></td></tr>'''
                for key in kwargs:
                    table +=  f'''<tr><td style="text-align:left">key :</td><td style="text-align:left">{key}</b>:{kwargs[key]}</td></tr> 
                </table></div>'''
            
            
                id = self.random_id
                msg =  f'''
                            <p>
                                <a href="#hidden_{id}" onclick="view('hidden_{id}'); return false"
                                style="color:green;text-decoration: none;">
                                            (+) --->
                                </a>
                            </p>  
                            <div id="hidden_{id}" style="display: none;">
                                            <p>{table}</p>
                            </div>
                            '''
                self.print(msg)
            except Exception as ex:
                self.print(f''' 
                какая - то хуйня 2
                {ex}
                ''')

            method_to_decorate(self , *args , **kwargs)
        return wrapper


       
      
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


       