
import re
import sys
import os
import random
import datetime
import time
from Ini import Ini
import DB as db
import execute_json as jsn



''' Вывод лога оформленного в HTML для Jypiter notebook '''
from IPython.display import display, HTML

class Log():
    
    def __init__(self,  **kwards):

        self.random_id = random.randint(0, 99999999)
        '''

        '''
        self.root = Ini().root
        self.logfile = str(f'''{self.root}\\Logging\\LOGS\\{self.random_id}.html''')
        # https://jugad2.blogspot.com/2015/09/find-caller-and-callers-caller-of.html
        # смотрим какая фгункция вызвала лог
        # https://www.linux.org.ru/forum/development/11297360
        # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch14s08.html
        #getframe_expr = 'sys._getframe({}).f_code.co_name'
        #caller =  str(f'''{eval(getframe_expr.format(3))}->
        #
        #{eval(getframe_expr.format(2))}''')# смотрим какая фгункция вызвала лог


        styles = str("<styles>")
        styles += str("<a { text-decoration: none; }")
        styles += str(".info { text-decoration: none; ")
        styles += str("         color:blue;")
        styles += str("         font-size:xx-small;}")
        styles += str("</styles>")
        self.print(styles)

        functions = str("<p>functions</p>")
        functions += str("<script>function view(n) {")
        functions += str("  style = document.getElementById(n).style;")
        functions += str("  style.display = (style.display == 'block') ? 'none' : 'block';")
        functions += str("}</script>")
        self.print(functions)
        pass

    def screenshot(self , log = object):
        log_str = str(log)
        filename =  str(self.current) + ".png"
        path_screenshot = f'''{self.root}/screenshots/{filename}'''
        print(f'''Saving { path_screenshot}''')
        #self.driver.get_screenshot_as_file(path)
        element = self.driver.find_element_by_tag_name('body')
        location = element.location
        size = element.size
        png = self.driver.get_screenshot_as_png() # saves screenshot of entire page
        element.screenshot(path)

        msg = str(f'''<a href="http://localhost:8888/notebooks/OneDrive/REPOS/LOG/{filename}" target="_blank">image</a>''')
        log_str += msg
        self.log(log_str)

    def print(self, msg = object, prn_type="simple"):
        #prn_type="jupiter"
        '''
        prn_type:"normal"|"simple"|"jupiter"
        '''
        if prn_type=="simple":
            print(re.sub(r'\<[^>]*\>', '', str(msg))) 
            return

        elif prn_type=="jupiter":
            display(
                HTML(
                    (f'''{str(msg)} ''')))
            return
        else:print(str(msg))
  
    def log(self ,  log = object):
        self.print(str(log))
        try:
            logfile = open(self.logfile  , mode = 'a' ,encoding = 'UTF-8')
            logfile.write(str(log))
            logfile.close()

        except Exception as ex:
            try:
                logfile = open(self.logfile  , mode = 'а' ,encoding = 'UTF-8')
                logfile.write(str(log))
                logfile.close()
                print(str({ex}))
            except Exception as ex:
                print(str({ex}))

    '''
    Декоратор
    Взято из https://habr.com/ru/post/141501/
    '''
    def logged(method_to_decorate):
        '''
        логирую задействованные в коде функции 
        '''
        def wrapper(self , *args , **kwargs):
            zadejstvovannye_funcii = ''
            getframe_expr = 'sys._getframe({}).f_code.co_name'
            try: zadejstvovannye_funcii += str(f'''->{eval(getframe_expr.format(6)) }''') ; 
            except:pass
            try: zadejstvovannye_funcii += str(f'''->{eval(getframe_expr.format(5)) }''') ; 
            except:pass
            try: zadejstvovannye_funcii += str(f'''->{eval(getframe_expr.format(4)) }''') ; 
            except:pass
            try: zadejstvovannye_funcii += str(f'''->{eval(getframe_expr.format(3)) }''') ; 
            except:pass
            try: zadejstvovannye_funcii += str(f'''->{eval(getframe_expr.format(2)) }''') ; 
            except:pass
            try: zadejstvovannye_funcii += str(f'''->{eval(getframe_expr.format(1)) }''') ; 
            except:pass
            try: zadejstvovannye_funcii += str(f'''->{eval(getframe_expr.format(0)) }''') ; 
            except:pass

            #исключаю wrapper
            zadejstvovannye_funcii = str(zadejstvovannye_funcii).split('->')

            id = random.randint(0, 1000000)

            title ='<span ><b>+</b>'
            for key in zadejstvovannye_funcii:
                if str(key) != 'wrapper': title += str(f'''{key}->''')
            title += str(f'''</span> ''')
            
            table = str(f'''<table style="color:black;font-size:x-small">
            <tr><td colspan=2 style="text-align:left">
            <b>args:</b></td></tr>''')
            i=1

            for arg in args:
                table += str(f'''<tr><td style="text-align:left">{i}.</td><td style="text-align:left">{arg}</td></tr> ''')
                i+=1
            table += str(f'''            <tr><td colspan=2 style="text-align:left">
            <b>kwargs:</b></td></tr>''')
            for key in kwargs:
                table += str(f''''<tr><td style="text-align:left">key :</td><td style="text-align:left">{key}</b>:{kwargs[key]}</td></tr> ''')
            table += str(f'''</table></div>''')

            msg = str(f'''
        <p>
            <a href="#hidden_{id}" onclick="view('hidden_{id}'); return false"
            style="color:green;text-decoration: none;">{title}</a>
        </p>  
        <div id="hidden_{id}" style="display: none;">
            <p>{table}</p>
        </div>
        ''')



            self.log(msg)

            method_to_decorate(self , *args , **kwargs)
        return wrapper

    def load(file , attrs='r'):
        '''
        Файл ЛОГ в директории 
        self.root}\\Logging\\LOGS\\
        '''
        logfile = open(f'''{self.root}\\..\\LOGS\\{file}'''  , mode = 'а' ,encoding = 'UTF-8')
        return logfile.read()




