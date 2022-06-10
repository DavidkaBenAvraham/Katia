from strings_formatter import StringFormatter as SF
from logging import Formatter
import selenium

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import selenium.webdriver as webdriver

import kora as kora
from kora.selenium import wd as kora_webdriver
from web_driver.google_search import GoogleHtmlParser as GoogleHtmlParser

from exceptions_handler import ExceptionsHandler as EH

''' 

################################################################################


                    НАЧАЛО


                      опции запуска драйверов 
                            Google, Mozilla
                            прописаны в файле
                            webdriver.json
      

'''
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
class Driver():
    ''' webriver 
    По умолчанию используется Firefox
    driver: вебдрайвер - (firefox, chrome, etc)
    wait: ожидание перед действиями селениума (нахуй не нужно)
    '''
    
   
    current_url : str = attrib(init = False , default = None)

    driver      : webdriver = attrib(init = False , default = None)
    
    get_parsed_google_search_result : GoogleHtmlParser = attrib(init = False, default = None)

    def __attrs_post_init__(self , *args, **kwrads):
        #self.set_driver(self.ini.webdriver_settings)
        pass

    def set_driver(self , webdriver_settings : dict) -> driver:      
        '''   webdriver_settings -  из своего launcher.json["webdriver"]
          
        kora = обертка для запуска в google.research
        взята из https://github.com/korakot/kora
        там также есть ИИ!
               
        и догружаю в kora нужные мне элементы из пакета selenium
        '''
        
        
       
        if webdriver_settings['name'] == 'kora':
            ''' kora - обёртка вебдрайвера для запуска в colab
            устанавливается в файле launcher '''

            self.driver = kora.selenium.wd
            self.driver.common = selenium.webdriver.common
            self.driver.support = selenium.webdriver.support
            
         

        if webdriver_settings['name'] == 'chromedriver': 
            options = webdriver.ChromeOptions()
            for argument in webdriver_settings["arguments"]:
                    options.add_argument(argument)
                    options.set_capability('intl.accept_languages', 'en-GB')
            self.driver = webdriver.Chrome(options = options)

        if webdriver_settings['name'] == 'firefox': 
                options = webdriver.FirefoxOptions()
                for argument in webdriver_settings["arguments"]:
                        options.add_argument(argument)
                        options.set_capability('intl.accept_languages', 'en-GB')
                self.driver = webdriver.Firefox(options = options)  


        if webdriver_settings['name'] == 'opera': 
            self.driver = webdriver.Opera(options = driver_options.opera_options(self))

        if webdriver_settings['name'] == 'edge': 
            self.driver = webdriver.Edge(options = driver_options.edge_options(self))

        if webdriver_settings['maximize_window'] : self.driver.maximize_window()

        self._wait = webdriver_settings['wait']

        self._add_extra_functions(webdriver_settings)

        return self.driver

    def _add_extra_functions(self ,webdriver_settings):
        
        self.driver.wait =                              self._wait
        self.driver.implicity_wait =                    self._implicity_wait
        self.driver.wait_to_precence_located =          self._wait_to_precence_located
        self.driver.wait_to_be_clickable =              self._wait_to_be_clickable
        self.driver.get_url =                           self._get_url
        self.driver.find =                              self._find
        self.driver.find_attributes_in_webelements =    self._find_attributes_in_webelements
        self.driver.parce_html_block =                  self._parce_html_block
        self.driver.click =                             self._click
        self.driver.page_refresh =                      self._page_refresh
        self.driver.close =                             self._close  
        self.driver.scroll =                            self._scroller
        
        self.driver.get_parsed_google_search_result =   GoogleHtmlParser
        self.driver.view_html_source_mode : bool =      webdriver_settings['view_html_source_mode']
        
    '''
                                    Ожидания драйвера



        Явное ожидание лучше чем time.sleep() ,  Но это не точно :)
    '''



    ''' ------------------ НАЧАЛО -------------------------- '''
    #@print
    def _implicity_wait(self , wait :int = 0):
        '''
        Неявное ожидание указывает WebDriver'у опрашивать DOM определенное количество времени, 
        когда пытается найти элемент или элементы, которые недоступны в тот момент. 
        Значение по умолчанию равно 0. После установки, неявное ожидание устанавливается 
        для жизни экземпляра WebDriver объекта.
        #self.wait = WebDriverWait(self.driver, kwargs.get('wait')) if 'wait' in kwargs else WebDriverWait(self.driver, 20)
        '''
        self.driver.implicitly_wait(wait)

    ''' ------------------ КОНЕЦ  -------------------------- '''




    ''' ------------------ НАЧАЛО -------------------------- '''
    #@print
    def _wait_to_precence_located(self, locator) -> object :
        '''
        ожидание 100% загрузки элемента
        locator=(By.CSS_SELECTOR , selector)
        '''
        return EC.presence_of_element_located(locator)
        
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- '''
    #@print
    def _wait_to_be_clickable(self, locator) :
        '''
        ождание кликабельности элемента '''
        element_clickable = EC.element_to_be_clickable(locator)
        webelement =  WebDriverWait(self.driver , wait).until(element_clickable)
        return webelement
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- '''

    #@print
    def _get_url(self, url:str )->bool:
        '''переход по заданному адресу 
        view_html_source = True : возвращает код страницы
        кроме того она проверяет что сайт не выпал в страницу логина
        '''


        def check_if_not_login():
            ''' проверяюм что не упал на логин 
            плохое решение. Драйверу нечего знать о поставщиках'''
            if str(self.driver.current_url).find(self.supplier_settings_from_json['login_url'])>0:
                self.related_functions.login(self)
            pass

        try:


            self.driver.get(f'''view-source:{url}''') if self.driver.view_html_source_mode else self.driver.get(f'''{url}''')
           
            self.driver.wait_to_precence_located(self, self.locators['body'])


            #check_if_not_login()
            ''' везде есть баги здесь проверка, что не выпала страница логина '''
            #self.driver._wait_to_precence_located(self, locator)

            if self.driver.current_url == 'about:blank':
                ''' если тормозит на пустой странице '''
                #self.driver.wait()
                self._get_url(url)
                pass
                ''' плохо реализовано - это костыль'''

            return True 
        except Exception as ex:
            return False , print(f''' Ошибка в _get_url() :
            {ex}
            -------------------------------------
            url = {url}''')
    

        #WebDriverWait(driver, 10).until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')
        #self.driver.execute_script('return document.readyState') == 'complete'
        ''' ожидание полной загрузки реализoваное на javascript'''
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- '''
    #@print
    def _scroller(self, wait : int =0 , prokrutok : int = 5, scroll_frame : int = 500) -> bool:
        ''' скроллинг '''
        try:
            for i in range(prokrutok):
                self.driver.execute_script(f'''window.scrollBy(0,{scroll_frame})''') # поднял окошко
                #time.sleep(wait)
                #self.wait(1)
            return True
        except Exception as ex: return  False , print(f''' ошибка скроллинга {ex}''')
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- '''   
    def _parce_html_block(self , html_block , locator):
        _elements = html_block.find_elements(locator['by'] , locator['selector'])
        return self._find_attributes_in_webelements(_elements , locator)

    ''' ------------------ КОНЕЦ  -------------------------- '''

    ''' ------------------ НАЧАЛО -------------------------- '''
    def _find_attributes_in_webelements(self , elements , locator): 
        '''аттрибуты в locator['attribute'] могут быть строкой  словарем или списком '''
        _е : list = [] 

        # 1) если аттрибуты в словаре {'href','text'}
        if str(type(locator['attribute'])).find('dict') >-1:
            _d  : dict = {}
            for k,v in dict(locator['attribute']).items():
                if str(type(elements)).find('list') >-1:
                    for el in list(elements): _d.update({el.get_attribute(k):el.get_attribute(v)})
                else: _d.update({elements.get_attribute(k):elements.get_attribute(v)})
            _е.append(_d)
            return _е

        #2) аттрибуты списоком ['href','text']
        if str(type(locator['attribute'])).find('list') >-1:
            for el in elements:
                for attr in locator['attribute']:_е.append(el.get_attribute(attr))
            return _е

        #3) один 'innerHTML'
        if str(type(locator['attribute'])).find('str') >-1:
            for el in elements:
                _е.append(el.get_attribute(locator['attribute']))
            return _е

        pass
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- ''' 
    #@print
    def _find(self, locator:dict):
        ''' поиск элементов на странице '''

        #1) выуживаю элементы со страницы
        elements = self._get_webelments_from_page(locator)

        #2) вытаскиваю аттрибуты по локатору
        return elements
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- '''   

    def _get_webelments_from_page(self, locator) ->list:
        try: elements = self.driver.find_elements(locator['by'] , locator['selector'])
        except Exception as ex: return [] , print(f''' ex: {ex} ''')
        return elements
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- '''   
    
    def _click(self, locator) ->bool:
        '''  Обработчик события click()  '''
            
        #element = self.wait_to_be_clickable(locator)
        #if element == False:

        try:element = self._find(self._wait_to_be_clickable(locator))
        except Exception as ex: return False , print(f''' Возникла ошибка поиска элемента {locator} ''')
        
        if element == False: return False , print(f''' Не Не нажался элемент {locator} ''')
        
        try: element.click() 
        except Exception as ex: return False , print(f''' Возникла ошибка - Не нажался элемент {locator} ''')

        return True ,  print(f''' Кликнул на {locator} ''')

        #if element == False:
        #    print(f''' Не нашёлся элемент {locator} ''')
        #    return False
        #try: element.click()
        #    return True
        #except : 
        #    print(f''' Не нажался элемент {locator} ''')
        #    return False
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- '''       
    def _page_refresh(self):
            '''
            Рефреш с ожиданием поной перезагрузки страницы
            '''
            self.driver.get_url(self.driver.current_url)
            pass
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- '''      
    def _close(self):
            if self.driver.close(): self.print(''' DRIVER CLOSED ''')
            pass



    ########################################  КОНЕЦ  #######################################
    




    ##@print 
    #def researh_webelements(self, elements)->bool:
    #    '''
    #    Функция для исследования элемента
    #    '''
    #    for element in elements:
         
    #        '''
    #        Исследование силами Селениума
    #        '''

    #        for attribute in element.get_attribute:
    #            self.print(f''' {attribute}  -  {element.get_attribute(attribute)}''')




    #        #log_str = f'''
    #        #Список HTML аттрибутов  элемента 
    #        #-----------------------------------------
    #        #Selenium:
    #        #type = {element.get_attribute('type')}
    #        #href = {element.get_attribute('href')}
    #        #id = {element.get_attribute('id')}
    #        #name = {element.get_attribute('name')}
    #        #title = {element.get_attribute('title')}
    #        #text = {element.get_attribute('text')}
    #        #value = {element.get_attribute('value')}
    #        #innerHTML = {element.get_attribute('innerHTML')}
    #        #outerHTML  = {element.get_attribute('outerHTML ')}
    #        #'''
            


    #        '''
    #        Исследование силами жаваскрипт
    #        '''

    #        attrs = self.driver.execute_script(f'''
    #        var items = {{}}; 
    #        for (index = 0; index < arguments[0].attributes.length; ++index)  
    #        {{ 
    #            items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value 
    #        }}; 
    #        return items;''', element)

    #        #attrs = self.driver.execute_script(f'''
    #        #var items = {}; 
    #        #for (index = 0; index < arguments[0].attributes.length; ++index)  
    #        #{ 
    #        #    items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value 
    #        #}; 
    #        #return items;''', element)

    #        log += f'''
    #        Javascript:
    #        -----------------------------------------
    #        {attrs} \n
    #        '''
    #        self.print(log)


    