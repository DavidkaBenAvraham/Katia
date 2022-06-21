# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia.Driver
##<h5>Типы вебдрайверов (не все!) </h5>
#<ul>
#<li>        webdriver.Firefox</li>
#<li>        webdriver.FirefoxProfile</li>
#<li>        webdriver.Chrome</li>
#<li>        webdriver.ChromeOptions</li>
#<li>        webdriver.Ie</li>
#<li>        webdriver.Opera</li>
#<li>        webdriver.PhantomJS</li>
#<li>        webdriver.Remote</li>
#<li>        webdriver.DesiredCapabilities</li>
#<li>        webdriver.ActionChains</li>
#<li>        webdriver.TouchActions</li>
#<li>        webdriver.Proxy</li>
#<li>        https://selenium-python.readthedocs.io/api.html#desired-capabilities</li>
#</ul>

from strings_formatter import StringFormatter
formatter = StringFormatter()
from logging import Formatter


import selenium
from selenium import * 
from selenium import webdriver as selenium_wedriver

#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
## from https://ru.stackoverflow.com/questions/1340290/%D0%A0%D0%B5%D0%B0%D0%BB%D0%B8%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-%D0%BA%D0%BB%D0%B8%D0%BA-%D0%BF%D0%BE-%D1%8D%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D1%83-%D0%B2-selenium-python

#import selenium.webdriver as webdriver

import kora 
from kora.selenium import wd as kora_wedriver

import seleniumwire
from seleniumwire import webdriver as seleniumwire_wedriver
# https://github.com/DavidkaBenAvraham/selenium-wire 

SWD = selenium_wedriver
KWD = kora_wedriver
SWWD = seleniumwire_wedriver
WD = SWD


from web_driver.google_search import GoogleHtmlParser as GoogleHtmlParser


#import html5lib
#from urllib.request import urlopen

#import xml.etree.ElementTree as ET
#from lxml import etree 
#from xml.etree import ElementTree as ET



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
    
    get_parsed_google_search_result : GoogleHtmlParser = attrib(init = False, default = None)

    driver : WD =  attrib(init = False , default = WD)

    ## <pre>
    # драйвер запускается через вызов set_driver(webdriver_settings)
    # при инициализации класса s = Supplier()
    # s.driver = Driver().set_driver(webdriver_settings : dict)
    # </pre>
    def __attrs_post_init__(self ,  *args, **kwrads):
        pass
    
    def set_driver(self , webdriver_settings : dict) -> WD:      
        
        def set_Chrome() -> dict:
            _settings = webdriver_settings['chrome']
            options = self.driver.ChromeOptions()
            for argument in _settings['arguments']:
                    options.add_argument(argument)
            self.driver = self.driver.Chrome(options = options)
            return _settings

        def set_Firefox() -> dict:
            _settings = webdriver_settings['firefox']
            options = webdriver.FirefoxOptions()
            for argument in webdriver_settings['firefox']['arguments']:
                    options.add_argument(argument)
            self.driver = webdriver.Firefox(options = options)
            return _settings


        def set_Kora() -> bool:
            _wd = kora.selenium.wd

            #options = _wd.ChromeOptions()
            #for argument in webdriver_settings['kora']:
            #        options.add_argument(argument)
            #self.driver = _wd.Chrome(options = options)

            return True

        if not kora.IN_COLAB: 
            print(f''' Hello local Jupiter :) ''')
            set_Firefox()
            self.driver.maximize_window()
        else:
            set_Chrome()
            print(f''' Hello colab ''')
        
        self.driver.wait =                              self._wait
        self.driver.get_url =                           self._get_url
        self.driver.find =                              self._find
        self.driver.find_attributes_in_webelements =    self._find_attributes_in_webelements
        self.driver.parce_html_block =                  self._parce_html_block
        self.driver.click =                             self._click
        self.driver.page_refresh =                      self._page_refresh
        self.driver.close =                             self._close  
        self.driver.scroll =                            self._scroller
        self.driver.previous_url        =               self.previous_url
        self.driver.get_parsed_google_search_result =   GoogleHtmlParser
        self.driver.send_keys =                         self._send_keys
        self.driver.JS =                                self.JS


        self.driver.WebKitGTK =                         SWD.WebKitGTK
        self.driver.WebKitGTKOptions =                  SWD.WebKitGTKOptions
        self.driver.WPEWebKit =                         SWD.WPEWebKit
        self.driver.WPEWebKitOptions =                  SWD.WPEWebKitOptions
        

        from selenium.webdriver.support.ui import WebDriverWait
        self.driver.WebDriverWait = WebDriverWait

        from selenium.webdriver.support import expected_conditions as EC
        self.driver.EC = EC

        from selenium.webdriver.common.by import By
        self.driver.By = By()

        from selenium.webdriver.common.keys import Keys
        self.driver.Keys = Keys()

        from selenium.webdriver.common.action_chains import ActionChains
        self.driver.ActionChains = ActionChains

        return self.driver



    def _wait(self , wait  = 0):
        if wait == 0 : wait = self._deafault_wait_time
        time.sleep(wait)
        pass


    ''' ------------------ НАЧАЛО -------------------------- '''
    #@print
    def _wait_to_precence_located(self, locator : dict ) -> object :
        '''
        ожидание 100% загрузки элемента
        locator=(By.CSS_SELECTOR , selector)
        '''
        return EC.presence_of_element_located(locator)
        
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- '''
    #@print
    
    def _wait_to_be_clickable(self, wait : int = 0 , locator : dict = {}) :
        '''
        ождание кликабельности элемента '''
        element_clickable = EC.element_to_be_clickable(locator)
        webelement =  WebDriverWait(self.driver , wait).until(element_clickable)
        return webelement
    

    ## переход по указанному url
    # обертка для driver.get()
    def _get_url(self, url:str , wait_to_locator_be_loaded : dict = {} , view_html_source_mode : bool = False)->bool:
        '''переход по заданному адресу 
        с ожиданием загрузки контента до локатора wait_locator_to_be_loaded
        view_html_source = True : возвращает код страницы
        кроме того она проверяет что сайт не выпал в страницу логина
        '''



        #''' КОСТЫЛЬ '''
        #if(len(wait_to_locator_be_loaded.items())) == 0:
        #    wait_to_locator_be_loaded = {
        #        "attribute": "innerHTML",
        #        "by": "tag name",
        #        "selector": "body"
        #        }
           

        _d = self.driver

        def check_if_not_login():
            ''' проверяюм что не упал на логин 
            плохое решение. Драйверу нечего знать о поставщиках'''

            if str(_d.current_url).find(self.settings['login_url'])>0:
                self.related_functions.login(self)
            pass

        try:
            _url = _d.current_url
            _d.get(f'''{url}''')
            _d.previous_url = _url
            
            main_window_handler = _d.current_window_handle
            ''' запоминаю рабочее окно
            далее я буду искать файлы json
            '''



            # Access requests via the `requests` attribute
            ##for request in _d.requests:
            ##    if request.response:
            ##        if str(request.response.headers['Content-Type']) == 'application/json':
            ##            print(
            ##                request.url,
            ##                request.response.status_code,
            ##                request.response.headers['Content-Type']
            ##                    )
           


            #if _d.current_url == 'about:blank':
            #    ''' если тормозит на пустой странице '''
            #    #self.driver.wait()
            #    self._get_url(url)
            #    pass
            #    ''' плохо реализовано - это костыль'''


            return True 
        except Exception as ex:
            return False , print(f''' Ошибка в _get_url() :
            {ex}
            -------------------------------------
            url = {url}''')
    

        #WebDriverWait(driver, 10).until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')
        #self.driver.execute_script('return document.readyState') == 'complete'
        ''' ожидание полной загрузки реализoваное на javascript'''
    
    def _scroller(self, wait : int = 0 , prokrutok : int = 12, scroll_frame : int = 1800) -> bool:
        ''' скроллинг '''
        try:
            for i in range(prokrutok):
                self.driver.execute_script(f'''window.scrollBy(0,{scroll_frame})''') # поднял окошко
                #time.sleep(wait)
                self._wait(0.1)
            return True
        except Exception as ex: return  False , print(f''' ошибка скроллинга {ex}''')
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- '''   
    def _parce_html_block(self , html_block , locator):
        _elements = html_block.find_elements(locator['by'] , locator['selector'])
        return self._find_attributes_in_webelements(_elements , locator)

    ''' ------------------ КОНЕЦ  -------------------------- '''

    ''' ------------------ НАЧАЛО -------------------------- '''
    def _find_attributes_in_webelements(self , elements , locator) -> list: 
        '''аттрибуты в locator['attribute'] 
        могут быть None, строкой,  словарем или списком 
         если аттрибут None - эта функция не должна вызываться,
         а вебэлемент отдается целиком '''


        _е : list = [] 
        _ = locator

        # 1) если аттрибуты в словаре {'href','text'}
        if isinstance(_['attribute']  , dict):
            if isinstance(elements , list):
                ''' элементы списком '''
                for el in elements: 
                    for k,v in dict(_['attribute']).items():
                        _е.append({el.get_attribute(k):el.get_attribute(v)})
            else:                     
                for k,v in dict(_['attribute']).items():
                    _е.append({elements.get_attribute(k):elements.get_attribute(v)})


        #2) аттрибуты списоком ['href','text']
        if isinstance(_['attribute']  , list):
            if isinstance(elements , list):
                ''' элементы списком '''
                for el in elements:
                    for attr in _['attribute']:
                        _е.append(el.get_attribute(attr))
            else: 
                for attr in _['attribute']:
                    _е.append(elements.get_attribute(attr))


        #3) один f.e. 'innerHTML'
        else:
            if isinstance(elements , list):
                ''' элементы списком '''
                for el in elements:_е.append(el.get_attribute(_['attribute']))
            else: _е.append(elements.get_attribute(_['attribute']))


        if len(_е) == 0:return None
        elif len(_е) == 1:return _е[0]
        else: return _е

    ''' ------------------ КОНЕЦ  -------------------------- '''

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

    

    def _get_webelments_from_page(self, locator) -> list:
        ''' возвращает найденные на странице элементы в списке элементы
        если элементы  не найдны -возвращает пустой список []
        '''
        try: 
            elements = self.driver.find_elements(locator['by'] , locator['selector'])
            return elements 
        except Exception as ex: return [] , print(f'''_get_webelments_from_page() ex: {ex} ''')
        
   
    def _click(self, locator) ->bool:
        ##  Обработчик события click()

        if isinstance(locator['selector'] , list):
            ## f.e. 
            #["//a[contains(@class,'address-select-trigger')]", "//li[contains(@data-code,'il')]"]

            for i in range(len(locator['selector'])):
                try: 
                    _ = {      
                        "attribute": None,
                        "by": "xpath",
                        "selector": locator['selector'][i]
                        }

                    _el = self._find(_)
                    if isinstance(_el , list): 
                        for e in _el: e.click()
                    else: _el.click()
                except Exception as ex: print(f''' Возникла ошибка  {ex} ''')
            return True

        try:element = self._find(locator)
        except Exception as ex:  return False , print(f''' Возникла ошибка {ex} поиска элемента {locator} ''') 
        
        if element == False:  return False , print(f''' Не найден элемент {locator} ''')
        
        try: element.click() 
        except Exception as ex: return False  , print(f''' Возникла ошибка  {ex} Не нажался элемент {locator} ''') 

        return True
   

    def _send_keys(self, locator , keys) ->bool:
        _ = locator
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


        except Exception as ex: return False , print(f''' ошибка {ex} при отправке {keys} в {locator} ''')
        
           
    def _page_refresh(self):
        ##Рефреш с ожиданием полной перезагрузки страницы
        self._get_url(self.driver.current_url)
        pass
  
    def _close(self):
            if self.driver.close(): self.print(''' DRIVER CLOSED ''')
            pass

        
