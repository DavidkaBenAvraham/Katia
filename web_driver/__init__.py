# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia.Driver
### Обертка 
# под капотом работают:
# selenium , kora , seleniumwire
# инерфейс самый простой - произвести простые комманды поймав
# локатором элемент
# 
##<h5>Типы поддерживаемых вебдрайверов (не все!) </h5>
#<ul>
#<li>        webdriver.Firefox</li>
#<li>        webdriver.Chrome</li>
#<li>        webdriver.Ie</li>
#<li>        webdriver.Opera</li>
#<li>        webdriver.PhantomJS</li>
#<li>        webdriver.Remote</li>
#</ul>
#<h5> Умеет в </h5>
#<ul>
#<li>        webdriver.DesiredCapabilities</li>
#<li>        webdriver.ActionChains</li>
#<li>        webdriver.TouchActions</li>
#<li>        webdriver.Proxy</li>
#<li>        https://selenium-python.readthedocs.io/api.html#desired-capabilities</li>
#</ul>

from pathlib import Path
from strings_formatter import StringFormatter
formatter = StringFormatter()
from logging import Formatter


import selenium
from selenium import * 


#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
## from https://ru.stackoverflow.com/questions/1340290/%D0%A0%D0%B5%D0%B0%D0%BB%D0%B8%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-%D0%BA%D0%BB%D0%B8%D0%BA-%D0%BF%D0%BE-%D1%8D%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D1%83-%D0%B2-selenium-python

#import selenium.webdriver as webdriver

import kora
import seleniumwire
from seleniumwire import webdriver as seleniumwire_wedriver
# https://github.com/DavidkaBenAvraham/selenium-wire 

import pickle


#from kora.selenium import wd as KWD

from selenium import webdriver as selenium_wedriver
SWD = selenium_wedriver
SWWD = seleniumwire_wedriver
WD = SWWD


#import html5lib
#from urllib.request import urlopen

#import xml.etree.ElementTree as ET
#from lxml import etree 
#from xml.etree import ElementTree as ET


import ast
#https://www.techiedelight.com/ru/parse-string-to-float-or-int-python/

import os
import pandas as pd
import datetime
import time

from logger import Log as log
from ini_files_dir import Ini as ini
import execute_json as json
from attr import attrs, attrib, Factory

@attrs
## класс <b>Driver()</b> 
# реализует функции selenium 
# в обертке 
# <a href="https://github.com/DavidkaBenAvraham/selenium-wire" target="_blank"
# style = "COLOR:#550000;FONT-SIZE:LARGE;FONT-DECORATION:BOLD" > 
# seleniumwire 
# </a>
# driver устанавливается из настроек в файле launcher.json, узел ['webdriver']
    # <h5>Например</h5>
    # <pre>
    #  "webdriver": {
    #    "name": "firefox",
    #    "arguments": [ "--no-sandbox", "--disable-dev-shm-usage" ],
    #    "disabled_arguments": [
    #      "--disable-dev-shm-usage",
    #      "--headless"
    #    ],
    #    "deafault_wait_time": 5,
    #    "maximize_window": true,
    #    "view_html_source_mode": false
    #}
    # </pre>
#<ul>
#<li>current_url : текущий url. Нужен мне для отслеживания переключений драйвера</li>
#<li>previous_url : прошлый url. Нужен мне для отслеживания переключений драйвера</li>
#<li>driver : webdriver </li>
#<li>get_parsed_google_search_result : время запуска скрипта</li>
#</ul>
class Driver:



    @attrs
    ### JS: Всякие javascrits полезности
    class JS():

        def unhide(driver,element):
            script :str = f''' arguments[0].style.opacity=1;
                            arguments[0].style['transform']='translate(0px, 0px) scale(1)';
                            arguments[0].style['MozTransform']='translate(0px, 0px) scale(1)';
                            arguments[0].style['WebkitTransform']='translate(0px, 0px) scale(1)';
                            arguments[0].style['msTransform']='translate(0px, 0px) scale(1)';
                            arguments[0].style['OTransform']='translate(0px, 0px) scale(1)';
                            arguments[0].scrollIntoView(true);
                            return true; '''

            self.super().Driver().driver.execute_script(script, element)

    ## текущий url. Нужен мне для отслеживания переключений драйвера
    current_url : str = attrib(init = False , default = None)

    ## прошлый url. Нужен мне для отслеживания переключений драйвера
    previous_url : str = attrib(init = False , default = None)
    

    #from web_drive.google_search import GoogleHtmlParser as GoogleHtmlParser

    #parsed_google_search_result : GoogleHtmlParser = attrib(init = False, default = GoogleHtmlParser)


    driver : WD =  attrib(init = False , default = WD)


    cookies = attrib(init = False , default = None)
    cookies_file_path : Path = attrib(init = False , default = Path('cookies.pkl'))
    
    
    ## <pre>
    # драйвер запускается через вызов set_driver(webdriver_settings)
    # при инициализации класса s = Supplier()
    # s.driver = Driver().set_driver(webdriver_settings : dict)
    # </pre>
    def __attrs_post_init__(self ,  *args, **kwrads):

        pass
    





    ## set_driver(webdriver_settings)
    # <pre>
    # webdriver_settings from launcher.json: 
    # --------------------------
    # f.e. FirefoxDriver
    #"firefox": {
    #     "arguments": [ "--no-sandbox" ],
    #     "disabled_arguments": [
    #       "--disable-dev-shm-usage",
    #       "--headless"
    #     ],
    #     "deafault_wait_time": 5,
    #     "about wait": "явное ожидание браузера в сек",
    #     "random": [ 0, 5 ],
    #     "view_html_source_mode": false,
    #     "maximize_window": true
    #   }
    # }
    # </pre>
    def set_driver(self , webdriver_settings : dict) -> WD:  
    

        ## set_Chrome
        def set_Chrome() -> bool:
            _settings = webdriver_settings['chrome']
            options = self.driver.ChromeOptions()
            for argument in _settings['arguments']:
                    options.add_argument(argument)
            self.driver = self.driver.Chrome(options = options)
            return True

        ## set_Firefox
        def set_Firefox() -> bool:
            _settings = webdriver_settings['firefox']
            options = self.driver.FirefoxOptions()
            for argument in _settings['arguments']:
                    options.add_argument(argument)
            self.driver = self.driver.Firefox(options = options)
            return True
         
        ## set_Kora
        def set_Kora() -> bool:
            _wd = kora.selenium.wd
            if not kora.IN_COLAB: 
                print(f''' Hello local  :) ''')
                set_Chrome()
                
            else:
                set_Chrome()
                print(f''' Hello colab ''')
                #options = _wd.ChromeOptions()
                #for argument in webdriver_settings['kora']:
                #        options.add_argument(argument)
                #self.driver = _wd.Chrome(options = options)

            return True


        #set_Firefox()
        set_Chrome()
        self.driver.maximize_window()



        self.driver.wait =                              self._wait
        self.driver.get_url =                           self._get_url
        self.driver.find =                              self._find
        self.driver.find_attributes_in_webelements =    self._find_attributes_in_webelements
        self.driver.parce_html_block =                  self._parce_html_block
        self.driver.click =                             self._click
        self.driver.page_refresh =                      self._page_refresh
        self.driver.close =                             self._close  
        self.driver.scroll =                            self._scroller
        self.driver.previous_url :str =                 self.previous_url
        self.get_dict_from_urlstr : dict =              self._get_dict_from_urlstr

        #self.driver.get_parsed_google_search_result =   GoogleHtmlParser
        self.driver.send_keys =                         self._send_keys
        self.driver.JS =                                self.JS
        
        
        self.driver.cookies =                           self.cookies
        self.driver.cookies_file_path :Path =           self.cookies_file_path
        self.driver.dump_cookies_to_file =              self._dump_cookies_to_file
        self.driver.load_cookies_from_file =            self._load_cookies_from_file


        self.driver.WebKitGTK =                         SWD.WebKitGTK
        self.driver.WebKitGTKOptions =                  SWD.WebKitGTKOptions
        self.driver.WPEWebKit =                         SWD.WPEWebKit
        self.driver.WPEWebKitOptions =                  SWD.WPEWebKitOptions
        

        from selenium.webdriver.support.ui import WebDriverWait
        self.driver.WebDriverWait = WebDriverWait

        from selenium.webdriver.support import expected_conditions as EC
        self.driver.EC = EC

        from selenium.webdriver.common.by import By
        self.driver.By = By

        from selenium.webdriver.common.keys import Keys
        self.driver.Keys = Keys

        from selenium.webdriver.common.action_chains import ActionChains
        self.driver.ActionChains = ActionChains

        return self.driver









    #########################################################
    #                                                       #
    #                                                       #
    #                       Ожидания                        #
    #                                                       #
    #                                                       #
    #########################################################

    ### _wait
    ## Явное ожидание через time.sleep
    def _wait(self , wait  = 0):
        if wait == 0 : wait = self._deafault_wait_time
        time.sleep(wait)
        pass


    ### _wait_to_precence_located 
    # ожидание 100% загрузки элемента
    def _wait_to_precence_located(self, locator : dict ) -> object :
        '''
        ожидание 100% загрузки элемента
        locator=(By.CSS_SELECTOR , selector)
        '''
        return self.EC.presence_of_element_located(locator)

    ## _wait_to_be_clickable 
    # ожидание кликабельности элемента
    def _wait_to_be_clickable(self, wait : int = 0 , locator : dict = {}) :
        '''
        ождание кликабельности элемента '''
        element_clickable = EC.element_to_be_clickable(locator)
        webelement =  WebDriverWait(self.driver , wait).until(element_clickable)
        return webelement
    















    #########################################################
    #                                                       #
    #                                                       #
    #                       Куки                            #
    #                                                       #
    #                                                       #
    #########################################################

    def _load_cookies_from_file(self, cookies_file_path : Path = None ) -> bool:
        ''' cookies_file_path if None = self.cookies_file_path '''

        try:
            cookies_file_path = self.cookies_file_path if cookies_file_path is None else cookies_file_path
            if not cookies_file_path.exists():
                return False , print(f''' {cookies_file_path} не найден ''')
            self.cookies = pickle.load(open(cookies_file_path , 'rb'))
            for cookie in self.cookies:
                self.driver.add_cookie(cookie)  
            return True
        except Exception as ex :     
            return False, print(f''' 
            ошибка в _load_cookies_from_file
            {ex}''') 

    ## После успешного события ведрайвера я бережно сохраню печеньку  в файл 
    #@param
    #   cookies_file : Path('cookies.pkl')
    def _dump_cookies_to_file(self, cookies_file_path : Path = None):
        cookies_file_path = self.cookies_file_path if cookies_file_path is None else cookies_file_path
        _cookies = self.driver.get_cookies()
        for cookie in _cookies:
            if cookie.get('expiry', None) is not None:
                cookie['expires'] = cookie.pop('expiry')
        pickle.dump(_cookies, open(cookies_file_path, 'wb'))





####################   driver.get() ###########################



    ## обертка для driver.get():
    # переход по указанному url
    # @param
    #   url:str 
    # @param
    #   view_html_source_mode : bool     возвращает код страницы
    def _get_url(self, url:str , wait_to_locator_be_loaded : dict = {} , view_html_source_mode : bool = False):
       
        
        _d = self.driver

        json_files : str = ''

        try:
            _url = _d.current_url
          
            _d.get(f'''{url}''')


            ## Здесь нерешенная проблема
            #if self.cookies is None : set_cookies()
            #_set_cookies()


            # запоминаю, где был
            _d.previous_url = _url

            # запоминаю рабочее окно 
            main_window_handler = _d.current_window_handle
            return True
            ### experimental:
            #<pre>
            #try:
            #    # Access requests via the `requests` attribute
            #    for request in _d.requests:
            #        if request.response:
            #            if str(request.response.headers['Content-Type']) == 'application/json':
            #                json_files += f'''
            #                    {str(request.url)}
            #                    {str(request.response.status_code)}
            #                    {str(request.response.headers['Content-Type'])}
            #                    '''
            #except:pass
            #finally:return  json_files
            #</pre>
        except Exception as ex:
            return False , print(f''' Ошибка в _get_url() :
            {ex}
            -------------------------------------
            url = {url}''')
    
        #ожидание полной загрузки реализoваное на javascript
        #WebDriverWait(driver, 10).until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')
        #self.driver.execute_script('return document.readyState') == 'complete'
        


    def _get_dict_from_urlstr(self)->dict:
        _url = self.current_url

        _url_str_to_list = str(_url).split(str(_url).find('?'))

        _params_str = f'''{{ {str(_url_str_to_list[1]).strip().replace('=' , ':' ,str(_url_str_to_list[1]))} }}'''
        
        _params = ast.literal_eval(_params_str)

        _d :dict = {"url":_url_str_to_list[0], "params":_params}

        return _d




    ## scroller
    def _scroller(self, wait : int = 0 , prokrutok : int = 5, scroll_frame : int = 1800) -> bool:
        ''' скроллинг '''
        try:
            for i in range(prokrutok):
                self.driver.execute_script(f'''window.scrollBy(0,{scroll_frame})''') # поднял окошко
                #time.sleep(wait)
                self._wait(0.1)
            return True
        except Exception as ex: return  False , print(f''' ошибка скроллинга {ex}''')
   

    ## parce_html_block
    def _parce_html_block(self , html_block , locator):
        _elements = html_block.find_elements(locator['by'] , locator['selector'])
        return self._find_attributes_in_webelements(_elements , locator)


    ## find_attributes_in_webelements
    def _find_attributes_in_webelements(self , elements , locator) -> list: 
        '''аттрибуты в locator['attribute'] 
        могут быть None, строкой,  словарем или списком 
         если аттрибут None - эта функция не должна вызываться,
         а вебэлемент отдается целиком '''


        _е : list = [] 
        _ = locator['attribute']

        # 1) если аттрибуты в словаре {'href':'text'}
        if isinstance(_  , dict):
            if isinstance(elements , list):
                ''' элементы списком '''
                for el in elements: 
                    for i in _.items():
                        _е.append({el.get_attribute(i[0]):el.get_attribute(i[1])})
            else:                     
                for k,v in _.popitem():
                    _е.append({elements.get_attribute(k):elements.get_attribute(v)})


        #2) аттрибуты списоком ['href','text']
        elif isinstance(_  , list):
            if isinstance(elements , list):
                ''' элементы списком '''
                for el in elements:
                    for attr in _:
                        _е.append(el.get_attribute(attr))
            else: 
                for attr in _:
                    _е.append(elements.get_attribute(attr))


        #3) один f.e. 'innerHTML'
        else:
            if isinstance(elements , list):
                ''' элементы списком '''
                for el in elements:
                    _е.append(el.get_attribute(_))
            else: _е.append(elements.get_attribute(_))
               

        if len(_е) == 0:return None
        elif len(_е) == 1:return _е[0]
        else: return _е

    
    ## FIND
    def _find(self, locator:dict) :
        ''' поиск элементов на странице 
        и поиск аттрибута по локатору (если он нужен)
         есть секрет в аттрибуте локатора
         если он пустой возвращается ВЕСЬ! элемент
        ----------------------------------------
        types of locator['attribute']:  str, None , [] , {}


        search for elements on the page and search for an attribute in the locator (if needed) 
        there is a secret: if the locator attribute if it is None (null in JSON), 
        ALL  element is be  returned! 
        ----------------------------------------
        types of locator['attribute']:  str, None , [] , {}
        '''

        # 0)
        '''
        в случае, когда элемент мне не нужен, но требуется по структуре
        построения сценария я заполняю локатор элемента значениями null
        '''

        if locator['attribute'] == 'current_url': return self.current_url
        if locator['by'] is None: return None




        ## 1) выуживаю элементы со страницы. 
        elements = self._get_webelments_from_page(locator)
        ## всегда получаю [] , но все равно проверяю 
        if isinstance(elements , list):
            if len(elements) == 1: 
                elements = elements[0]
                ''' все таки я решил единственный найденный элемент не передавать списком '''
            elif len(elements) == 0:  
                elements = None
                return None
                ''' пустой список - вебдрайвер  не нашел элемент
                Нет смысла продолжать функцию '''
            else: pass # все норм. Пришел список
           
        

        ## 2) Если локатор locator['attribute'] не установлен в None 
        # то я возвращаю аттрибуты полученные по этому локатору
        # иначе - возвращаю весь найденный webelement
        # херовенько возвращать разные типы данных из функции, но мне так удобно
        return elements if  locator['attribute'] is None else self._find_attributes_in_webelements(elements , locator)

    ## get_webelments_from_page
    def _get_webelments_from_page(self, locator) -> list:
        ''' возвращает найденные на странице элементы в списке элементы
        если элементы  не найдны -возвращает пустой список []
        '''
        try: 
            elements = self.driver.find_elements(locator['by'] , locator['selector'])
            return elements 
        except Exception as ex: return None , print(f'''_get_webelments_from_page() 
        locator['by'] , locator['selector']  {locator['by']} , {locator['selector']}
        ex: {ex} ''')
        
    ## CLICK
    ##  Обработчик события click()
    def _click(self, locator) ->bool:
        

        
        _url_before_click = self.current_url
        ''' Запоминаю url ДО клика '''

        def err_handler():
            pass

        if isinstance(locator['selector'] , list):
            for i in range(len(locator['selector'])):
                try: 
                    # создаю подлокатор
                    _ = {      
                        "attribute": None,
                        "by": "xpath",
                        "selector": locator['selector'][i]
                        }
                    _el = self._find(_)
                    ## Я могу получить несколько элементов
                    # так устроена система: я жадно собираю со страницы 
                    # ВСЕ элементы по локатору
                    if isinstance(_el , list): 
                            for e in _el: 
                                try: e.click()
                                except Exception as ex: print(f''' 
                                Возникла ошибка  {ex} 
                                ----------------------
                                элемент:
                                {e} ne обязательно должен нажиматься
                                он часть списка 
                                {_el}
                                ''')
                                continue
                    else: 
                        _results : Factory(list) = []
                        try: 
                            _el.click()
                            _results.append(True)
                        except Exception as ex: 
                            print(f''' 
                                Возникла ошибка  {ex} 
                                ----------------------
                                элемент:
                                {_el} не нажался
                                --------
                                я попробую достучаться до него посылая Key.Return
                                ''')
                            try:self._send_keys( _ , self.driver.Keys.RETURN)
                            except Exception as ex: print(f'''   ХУЙ! ''')
                except Exception as ex: 
                            print(f''' 
                                Возникла ошибка  {ex} 
                                ----------------------
                                элемент:
                                {_el} не нажался
                                --------
                                я попробую достучаться до него посылая Key.Return
                                ''')
                            try:self._send_keys( _ , self.driver.Keys.RETURN)
                            except Exception as ex: print(f'''   ХУЙ! ''')
            return True

        try: _e = self._find(locator)
        except Exception as ex:  return False , print(f''' Возникла ошибка {ex} поиска элемента {locator} ''') 
        
        
        try:
            _e.click()
            
            #если после клика изменился url
            #    запоминаю изменения
            if _url_before_click != self.current_url:
                self.previous_url = _url_before_click

        except Exception as ex: 
                            print(f''' 
                                Возникла ошибка  {ex} 
                                ----------------------
                                элемент:
                                {_e} не нажался
                                --------
                                я попробую достучаться до него посылая Key.Return
                                ''')
                            try:self._send_keys( _ , self.driver.Keys.RETURN)
                            except Exception as ex: print(f'''   ХУЙ! ''')
        return True
    ## SEND KEYS
    def _send_keys(self, keys , locator : dict ='' , el  = None) ->bool:
        _ = locator
        _url_before_send_keys = self.current_url
        ''' Запоминаю url ДО клика '''
        try:
            if isinstance(_['selector'] , dict):
                #пока не использую
                pass
            elif isinstance(_['selector'] , list):
                for i in range(len(_['selector'])):
                    _l : dict = {
                        "attribute": _['attribute'][i],
                        "by": _['by'],
                        "selector": _['selector'][i]}
                    _el = self._find(_l)
                    _el.send_keys(keys)
            else: self._find(_).send_keys(keys)

            #если после клика изменился url
            #    запоминаю изменения
            if _url_before_send_keys != self.current_url:
                self.previous_url = _url_before_send_keys


        except Exception as ex: return False , print(f''' ошибка {ex} при отправке {keys} в {locator} ''')
    ## PAGE REFRESH      
    def _page_refresh(self):
        ##Рефреш с ожиданием полной перезагрузки страницы
        self._get_url(self.driver.current_url)
        pass
    ## CLOSE
    def _close(self):
            if self.driver.close(): self.print(''' DRIVER CLOSED ''')
            pass

        
