from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


from kora.selenium import wd
#from kora.selenium.wd.common.by import By
#from kora.selenium.wd.support.ui import WebDriverWait
#from kora.selenium.wd.support import expected_conditions as EC
#from kora.selenium.wd.common.keys import Keys

import kora as kora


#from urllib.request import urlopen
#import urllib

from exceptions_handler import ExceptionsHandler

''' ################################################################################
                      опции запуска драйверов 
                            Google, Mozilla
                            прописаны в файле
                            webdriver.json
      

'''
import os
import pandas as pd
import datetime
import time

import html5lib
from urllib.request import urlopen

#import xml.etree.ElementTree as ET
#from lxml import etree 
#from xml.etree import ElementTree as ET

from logger import Log
from ini_files import Ini
import execute_json as jsn
import json

from attr import attrs, attrib, Factory


@attrs
class Driver(Log):
    ''' webriver 
    По умолчанию используется Firefox
    driver: вебдрайвер - (firefox, chrome, etc)
    wait: ожидание перед действиями селениума (нахуй не нужно)
    '''
    driver : webdriver = attrib(init = False)
    current_url : str = attrib(init = False)
    print_response_status_code : str = attrib(init = False)
    kora_driver : kora.selenium.wd = attrib(init=False)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self.set_driver()
        

       
    @Log.log_f
    def set_driver(self , kora  = True):      
        '''запускаю вебдрайвер по сценарию из webdriver.json'''

        if kora : 
            self.driver = wd
            return self

        d = jsn.loads(self.path_ini / 'webdriver.json')["driver"]


        if d['name'] == 'chromedriver': 
            options = webdriver.ChromeOptions()
            for argument in d["arguments"]:
                    options.add_argument(argument)
            self.driver = webdriver.Chrome(options = options)

        if d['name'] == 'firefox': 
                options = webdriver.FirefoxOptions()
                for argument in d["arguments"]:
                        options.add_argument(argument)
                self.driver = webdriver.Firefox(options = options)  


        if d['name'] == 'opera': self.driver = webdriver.Opera(options = driver_options.opera_options(self))
        if d['name'] == 'edge': self.driver = webdriver.Edge(options = driver_options.edge_options(self))
        self.driver.maximize_window()
        return self







    #@Log.log_f
    #def html2json(self , html : str = '')->json:
    #    ''' конвертирую  html в json объект
    #   по умолчанию html хранится в
    #   self.driver.page_source
    #    '''
    #    if html == '': html = self.driver.page_source
    #    _json = xmltojson.parse(html)
    #    return _json



    '''








                                    Ожидания драйвера









    '''



    #@Log.logged 
    def driver_implicity_wait(self , wait):
        '''
        Неявное ожидание указывает WebDriver'у опрашивать DOM определенное количество времени, 
        когда пытается найти элемент или элементы, которые недоступны в тот момент. 
        Значение по умолчанию равно 0. После установки, неявное ожидание устанавливается 
        для жизни экземпляра WebDriver объекта.
        #self.wait = WebDriverWait(self.driver, kwargs.get('wait')) if 'wait' in kwargs else WebDriverWait(self.driver, 20)
        '''
        self.driver.implicitly_wait(wait)
        
    #@Log.log_f    
    def wait(self , wait_in_seconds):
        '''
        Явное ожидание
        лучше чем time.sleep()
        '''
        WebDriverWait(self.driver, wait_in_seconds)
        time.sleep(wait_in_seconds)

    #@Log.log_f 
    def wait_to_precence_located(self, locator):
        '''
        locator=(By.CSS_SELECTOR , selector)
        '''
        self.print(f''' Ждём локатор {locator} ''')
        element_precence_located = EC.presence_of_element_located(locator)
        return element_precence_located
        pass

    #@Log.log_f 
    def wait_to_be_clickable(self, locator, time_to_wait = 5):
        element_clickable = EC.element_to_be_clickable(locator)
        try:
            return WebDriverWait(self.driver , time_to_wait).until(element_clickable)
        except TimeoutException as ex:
            self.print(f''' не получила ответ от {element_clickable}  ''')
            self.log(ex)
            return False






    #@Log.log_f
    #def normalize_dom(self , raw_html : str = '')->json:
    #    ''' конвертирую  html в json объект
    #   по умолчанию html хранится в
    #   self.driver.page_source
    #    '''
    #    html  =  html5lib.parse(raw_html, treebuilder="lxml")
    #    #tree = etree.parse(StringIO(html))
    #    return xml





    '''             Переход по адресу           '''


    #@Log.logged 
    def get_url(self, url):

        try:


            self.driver.prev_url = self.driver.current_url
            #self.driver.get(f'''view-source:{url}''')
            self.driver.get(f'''{url}''')
            #self.normalize_dom(self.driver.page_source)
            
            #WebDriverWait(driver, 10).until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')
            #self.log( f'''Страница загрузилась : {self.driver.current_url}''')

            return True
        except Exception as eх: 
            self.print(f''' 
            Ошибка {eх} 
            по адресу {url} ''' )
            return False








    

    '''                     
    
    
                                Поиск элементов         
                                Поиск элементов по локатору на странице HTML 
                        Локаторы заданы в файле <префикс поставщика>.json

                                locator=(By.CSS_SELECTOR , selector)
                                функция поиска элементов заменяющая
                                driver.find_element_by_
                                                        css_selector
                                                        id
                                                        xpath
                                                        ...




        
                                мой локатор имеет три аргеумнта
                                'attribute': 'href', 
                                'by': 'xpath', 
                                'selector': ''
                                --------------

                                #if research: 


                                           research - опция исследования полученного элемента
 
                                            
'''
    @Log.log_f
    def find(self, locator:dict ) -> []:


        #_driver_wait  :int = 1
        # может вернуться или один или несколько элементов списком
        element = WebDriverWait(self.driver, int(_driver_wait)).until(EC.presence_of_element_located((locator)))
        elements = WebDriverWait(self.driver, int(_driver_wait)).until(EC.presence_of_all_elements_located((locator)))
      
            
            
            
        '''
                                        Возвращает  СПИСОК элементов
        '''
            

        #   1) Если нашлось несколько
        if len(elements) >= 1: 
            self.print(elements)
            return elements

        #   2) Если один строкой
        elif str(type(element)).find("webelement") >-1:
            self.print(element)
            return [element]
            
        #   3) ни одного
        else: 
            self.print("ХУЙ")
            return []
    
    @Log.log_f 
    def click(self, locator):
        element = self.wait_to_be_clickable(locator)
        if element == False:
            element = self.find(locator)
            if element == False:
                self.print(f''' Не нажался элемент {locator} ''')
                return False
            try: element.click()
            except : 
                self.print(f''' Не нажался элемент {locator} ''')
                return False


    @Log.log_f 
    def page_refresh(self):
        '''Рефреш с ожиданием поной перезагрузки страницы
        '''
        self.driver.get_url(self.driver.current_url)
        pass
    
    @Log.log_f 
    def close(self):
        if self.driver.close(): self.print(''' DRIVER CLOSED ''')
        pass

    




    #@Log.logged
    def get_elements_by_locator(self, locator) ->[]:
        '''
        возвращает список значений аттрибута элементов найденных по локатору <locator:dict()> 
        
        Словарь locator содержит три элемента:


                - "by": "xpath",
                    шаблон поиска
                        Примеры шаблонов:
                    - xpath
                    - css selector

                    


                - "selector": "//li[@data-value='ru']"
                    селектор элемента
                        Примеры селекторов
                    - //li[@data-value='en']
                    - //a[contains(@class,'MuiTypography') and contains(@href , 'web/item')]
                    - //*[@id='product-page-root']//div[@aria-label]/p
                    - //*[@id='product-page-root']//div[@aria-label]//following-sibling::div/p[1]


                - "attribute": "sendKeys(Keys.RETURN)",
                    обработка полученного элемента
                            Примеры аттрибутов:
                    - href
                    - a
                    - text
                    - innerHTML
                    - innerText
                    - sendKeys(Keys.RETURN)

        etc.
        '''
        try:
            res = []


            elements = self.find((locator['by'],locator['selector']))
            '''
                может получить список элементов или один элемент или хуй

                Функция  возвращает список [] или False


            '''
            if len(elements) == 0: return False

            if str(type(elements)).find("class 'list'") >-1:
                '''если нашлось несколько 
                элементов по указанному локатору '''
                
                for element in elements:
                    attriute = element.get_attribute(locator['attribute'])
                    res.append(attriute)
                return res

            elif str(type(elements)).find("WebElement") >-1: 
                '''
                если нашелся только один
                '''
                attriute = element.get_attribute(locator['attribute'])
                res.append(attriute)
                return res
        except Exception as ex: 
            self.print(f'''Ошибка в функции 
            get_elements_by_locator(self)
            {ex}''')
            return []




























































































    #@Log.logged 
    def researh_elements(self, elements)->bool:
        '''
        Функция для исследования элемента
        '''
        for element in elements:
         
            '''
            Исследование силами Селениума
            '''
            log_str = f'''
            Список HTML аттрибутов  элемента 
            -----------------------------------------
            Selenium:
            type = {element.get_attribute('type')}
            href = {element.get_attribute('href')}
            id = {element.get_attribute('id')}
            name = {element.get_attribute('name')}
            title = {element.get_attribute('title')}
            text = {element.get_attribute('text')}
            value = {element.get_attribute('value')}
            innerHTML = {element.get_attribute('innerHTML')}
            outerHTML  = {element.get_attribute('outerHTML ')}
            '''
            
            '''
            Исследование силами жаваскрипт
            '''
            attrs = self.driver.execute_script('''
            var items = {}; 
            for (index = 0; index < arguments[0].attributes.length; ++index)  
            { 
                items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value 
            }; 
            return items;''', element)

            log += f'''
            Javascript:
            -----------------------------------------
            {attrs} \n
            '''
            self.print(log)



