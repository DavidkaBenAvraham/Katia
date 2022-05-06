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

    def print(self, log = object , prn_type:str=''):
        '''  Вывод в консоль
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
        '''запись лога  в файл 
        self.path_log_file
        '''
        open(self.path_log_file  , mode = '+a' ,encoding = 'UTF-8').write(str(log))



       