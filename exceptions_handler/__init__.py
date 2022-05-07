from attr import attrs, attrib, Factory
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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import selenium.common.exceptions


'''

    https://ru.stackoverflow.com/questions/690959/%d0%b4%d0%b5%d0%ba%d0%be%d1%80%d0%b0%d1%82%d0%be%d1%80-%d0%b4%d0%bb%d1%8f-%d0%be%d0%b1%d1%80%d0%b0%d0%b1%d0%be%d1%82%d0%ba%d0%b8-%d0%be%d1%88%d0%b8%d0%b1%d0%be%d0%ba/690963#690963

    import random


    def my_decorator(fn):
        def wrapped():
            try:
                return fn()
            except Exception as e:
                print("Error:", e)

        return wrapped


    @my_decorator
    def my_func():
        while True:
            if random.randint(0, 4) == 0:
                raise Exception('Random!')

            print('Ok')


    my_func()
'''

@attrs
class ExceptionsHandler():

    def __attrs_post_init__(self):
        pass


    '''
    
                                Декоратор обработчика ошибок

                                все события try:, except:, finally: обрабатываются здесь

                                Декоратор

    '''

    def handler(fn):
        ''' декоратор - перехватчик исключений  '''
        try: 
            return fn
        except Exception as ex:
            print(f'''{ex}''')
            return false #fn(*args , **kwargs)

                {eх}
                '''
                )
        


        #def wrapped(self):
            
        #    #try:
        #    #    return fn

        #    #except NoSuchElementException as eх:msg(ex,fn)

        #    #except InvalidSessionIdException as ex:msg(ex,fn)

        #    #except StaleElementReferenceException as ex:msg(ex,fn)

        #    #except InvalidArgumentException as ex:msg(ex,fn)

        #    #except TimeoutException as ex:msg(ex,fn)

        #    #except ElementClickInterceptedException as ex: msg(ex,fn)

        #    #except Exception as ex:msg(ex,fn)
           
        #    #finally:
        #    #    pass

        #return wrapped

   