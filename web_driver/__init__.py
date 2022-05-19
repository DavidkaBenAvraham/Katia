import selenium

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import selenium.webdriver as webdriver

import kora as kora
from kora.selenium import wd as wd


from exceptions_handler import ExceptionsHandler as EH

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

#import html5lib
#from urllib.request import urlopen

#import xml.etree.ElementTree as ET
#from lxml import etree 
#from xml.etree import ElementTree as ET

from logger import Log
from ini_files_dir import Ini
import execute_json as json
from attr import attrs, attrib, Factory


@attrs
class Driver():
    ''' webriver 
    По умолчанию используется Firefox
    driver: вебдрайвер - (firefox, chrome, etc)
    wait: ожидание перед действиями селениума (нахуй не нужно)
    '''
    
    kora : kora = attrib(init = False , default = kora)
    #ini : ini = attrib(kw_only = True , default = None)
    current_url : str = attrib(init = False , default = None)
    #print_response_status_code : str = attrib(init = False)
    driver : kora_webdriver = attrib(init=False , default = kora_webdriver)
    #kora_driver.common : selenium.webdriver.common = attrib(init= False)
    wait : int = attrib(init = False, default = None)
    webdriver_settings : json = attrib(init = False , default = None)

    def __attrs_post_init__(self , *srgs, **kwrads):
        self.set_driver(self.ini.webdriver_settings)

    def set_driver(self , webdriver_settings : dict) -> driver:      
        '''   webdriver_settings - установки драйвера не из файла, а из своего json
            или запускаю вебдрайвер по сценарию из launcher.json["webdriver"]

        kora = обертка для запуска в google.research
        взята из https://github.com/korakot/kora
        там также есть ИИ!
               
        и догружаю в kora нужные мне элементы из пакета selenium
        '''

        #_driver_settings = webdriver_settings
        ''' устанавливается в файле launcher '''       
       
        if webdriver_settings['name'] == 'kora':
            ''' устанавливается в файле launcher '''

            self.driver = kora.selenium.wd
            self.driver.common = selenium.webdriver.common
            self.driver.support = selenium.webdriver.support

            #self.driver.support.ui.WebDriverWait = selenium.webdriver.support.ui.WebDriverWait
            #self.driver.support.expected_conditions = selenium.webdriver.support.expected_conditions
            #self.driver.common.keys = selenium.webdriver.common.keys
            #self.driver.common.by =  selenium.webdriver.common.by
            return self.driver




        ''' все остальное касается запуска драйвера selenium с моими установками '''




        if webdriver_settings['name'] == 'chromedriver': 
            options = webdriver.ChromeOptions()
            for argument in webdriver_settings["arguments"]:
                    options.add_argument(argument)
            self.driver = webdriver.Chrome(options = options)

        if webdriver_settings['name'] == 'firefox': 
                options = webdriver.FirefoxOptions()
                for argument in webdriver_settings["arguments"]:
                        options.add_argument(argument)
                self.driver = webdriver.Firefox(options = options)  


        if webdriver_settings['name'] == 'opera': 
            self.driver = webdriver.Opera(options = driver_options.opera_options(self))

        if webdriver_settings['name'] == 'edge': 
            self.driver = webdriver.Edge(options = driver_options.edge_options(self))

        #self.driver.maximize_window()
        return self.driver



    


    '''








                                    Ожидания драйвера





    '''



    #@Log.log
    def implicity_wait(self , wait :int = 0):
        '''
        Неявное ожидание указывает WebDriver'у опрашивать DOM определенное количество времени, 
        когда пытается найти элемент или элементы, которые недоступны в тот момент. 
        Значение по умолчанию равно 0. После установки, неявное ожидание устанавливается 
        для жизни экземпляра WebDriver объекта.
        #self.wait = WebDriverWait(self.driver, kwargs.get('wait')) if 'wait' in kwargs else WebDriverWait(self.driver, 20)
        '''
        if wait == 0 : wait = self.wait
        self.driver.implicitly_wait(wait)
        
    #@Log.log   
    def wait(self , wait : int = 0):
        '''
        Явное ожидание
        лучше чем time.sleep()
        '''
        WebDriverWait(self.driver, wait if not wait == 0 else self.wait)
        #time.sleep(wait_in_seconds)

    #@Log.log
    def wait_to_precence_located(self, locator):
        '''
        ожидание 100% загрузки элемента
        locator=(By.CSS_SELECTOR , selector)
        '''
        self.print(f''' Ждём локатор {locator} ''')
        element_precence_located = EC.presence_of_element_located(locator)
        return element_precence_located
        pass

    #@Log.log
    def wait_to_be_clickable(self, locator, wait : int = 0):
        '''
        ождание кликабельности элемента '''
        element_clickable = EC.element_to_be_clickable(locator)
        return WebDriverWait(self.driver , wait).until(element_clickable)



    '''             
    
      
    
                                        Переход по адресу           
                                        функция get_url()
                                        
                                        
                                        '''

    
    #@Log.log 
    def get_url(self, url)->bool:
        '''умный? переход по заданному адресу '''

        self.driver.prev_url = self.driver.current_url
        self.driver.get(f'''{url}''')
        #self.driver.get(f'''view-source:{url}''') <--- можно и так
        
        



        #WebDriverWait(driver, 10).until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')
        ''' ожидание полной загрузки
        реализoвано на javascript
        self.driver.execute_script('return document.readyState') == 'complete'
        '''



        return True







    

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
        #@Log.log
        #@EH.exeptions_handler
    def find(self, locator:dict ) -> []:


            '''
            By ->
                    CLASS_NAME	'class name'	str
		            CSS_SELECTOR	'css selector'	str
		            ID	'id'	str
		            LINK_TEXT	'link text'	str
		            NAME	'name'	str
		            PARTIAL_LINK_TEXT	'partial link text'	str
		            TAG_NAME	'tag name'	str
		            XPATH	'xpath'	str
            '''

            #by = By = self.driver.common.by.By
            #EC = self.driver.support.expected_conditions


            # element = self.driver.find_element(locator['by'] , locator['selector'])
            elements = self.driver.find_elements(locator['by'] , locator['selector'])


            def with_wait():
                _driver_wait  :int = self.ini.webdriver_settings["wait"] # вообще-то задается в файле webdriver.json
                try:elements = WebDriverWait(self.driver, int(_driver_wait)).until(EC.presence_of_all_elements_located((locator['by'], locator['selector'])))    
                except:elements = element = WebDriverWait(self.driver, int(_driver_wait)).until(EC.presence_of_element_located((locator['by'], locator['selector'])))
                
            '''

                                        
        
                                        Неважно, сколько нашел вебдравер
                                        я Всегда возвращаю  СПИСОК элементов



            '''
            

            #   1) Если нашлось несколько
            if len(elements) >= 0: 
                attrs : [] = []
                for el in elements: attrs.append(el.get_attribute(locator['attribute']))
                return attrs

            #   2) Если один строкой
            elif str(type(element)).find("webelement") >-1:
                #self.print(element)
                return [element.get_attribute(locator['attribute'])]
            
            #   3) ни одного
            else: 
                self.print("ХУЙ")
                return []
    
        #@Log.log
    def click(self, locator):
            '''
            Обработчик события click()
            '''
            element = self.wait_to_be_clickable(locator)
            if element == False:
                element = self.find(locator)
                if element == False:
                    self.print(f''' Не нашёлся элемент {locator} ''')
                    return False
                try: element.click()
                except : 
                    self.print(f''' Не нажался элемент {locator} ''')
                    return False


        #@Log.log 
    def page_refresh(self):
            '''
            Рефреш с ожиданием поной перезагрузки страницы
            '''
            self.driver.get_url(self.driver.current_url)
            pass
    
        #@Log.log 
    def close(self):
            if self.driver.close(): self.print(''' DRIVER CLOSED ''')
            pass

    




    #@Log.log
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

            res = []

            elements = self.find((locator['by'],locator['selector']))
            '''
                может получить список элементов или один элемент или хуй

                Функция  возвращает список [] или False


            '''
            if len(elements) == 0: return []

            if str(type(elements)).find("class 'list'") >-1:
                '''если нашлось несколько 
                элементов по указанному локатору '''
                
                for element in elements:
                    attribute = element.get_attribute(locator['attribute'])
                    res.append(attribute)
                return res

            elif str(type(elements)).find("WebElement") >-1: 
                '''
                если нашелся только один
                '''
                attribute = element.get_attribute(locator['attribute'])
                res.append(attribute)
                return res





    #@Log.log 
    def researh_webelements(self, elements)->bool:
        '''
        Функция для исследования элемента
        '''
        for element in elements:
         
            '''
            Исследование силами Селениума
            '''

            for attribute in element.get_attribute:
                self.print(f''' {attribute}  -  {element.get_attribute(attribute)}''')




            #log_str = f'''
            #Список HTML аттрибутов  элемента 
            #-----------------------------------------
            #Selenium:
            #type = {element.get_attribute('type')}
            #href = {element.get_attribute('href')}
            #id = {element.get_attribute('id')}
            #name = {element.get_attribute('name')}
            #title = {element.get_attribute('title')}
            #text = {element.get_attribute('text')}
            #value = {element.get_attribute('value')}
            #innerHTML = {element.get_attribute('innerHTML')}
            #outerHTML  = {element.get_attribute('outerHTML ')}
            #'''
            


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


    