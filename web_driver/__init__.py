from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
import urllib

from exceptions_handler import ExceptionsHandler
#from html2json import collect

''' ################################################################################

Объединил возможности selenium.webdriver и urllib.request




##########################################
        опции запуска драйверов 
        Google, Mozilla
        прописаны в файле
        webdriver.json

'''
#import Driver.driver_options as driver_options
import os
import pandas as pd
import datetime
import time

from logger import Log
from ini_files import Ini
import execute_json as jsn
import json




from attr import attrs, attrib, Factory

@attrs
class Driver(Log):
    '''
    Работа с вебдрайвером
    По умолчанию используется Firefox
    driver: имя драйвера (firefox, chrome, etc)
    wait: ожидание перед действиями селениума
    '''
    driver : webdriver = attrib(init = False)
    current_url : str = attrib(init = False)
    print_response_status_code : str = attrib(init = False)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self.set_driver()
        
    
       
    
    def set_driver(self):      
        '''запускаю вебдрайвер по сценарию из webdriver.json'''
        try:
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
        except Exception as ex: 
            self.print(f''' Ошибка запуска драйвера {ex} ''')
            return False

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
        
    #@Log.logged    
    def wait(self , wait_in_seconds):
        '''
        Явное ожидание
        лучше чем time.sleep()
        '''
        WebDriverWait(self.driver, wait_in_seconds)
        time.sleep(wait_in_seconds)

    #@Log.logged 
    def wait_to_precence_located(self, locator):
        '''
        locator=(By.CSS_SELECTOR , selector)
        '''
        self.print(f''' Ждём локатор {locator} ''')
        element_precence_located = EC.presence_of_element_located(locator)
        return element_precence_located
        pass

    #@Log.logged 
    def wait_to_be_clickable(self, locator, time_to_wait = 5):
        element_clickable = EC.element_to_be_clickable(locator)
        try:
            return WebDriverWait(self.driver , time_to_wait).until(element_clickable)
        except TimeoutException as ex:
            self.print(f''' не получила ответ от {element_clickable}  ''')
            self.log(ex)
            return False

    def html2json(self)->json:
        return xmltojson.parse(self.driver.page_source)

    '''             Переход по адресу           '''


    def get_url(self, url:str, 
                headers:dict={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0'},
                ) :
        ''' перехожу по указанному урл
        и вытаскиваю HTML и JSON
        '''
        self.driver.prev_url = self.driver.current_url
        self.driver.get(url)
        self.print_driver_response_code()
        return self.driver.page_source 
    

    '''                     Поиск элементов         '''

    def find(self, locator:dict ) -> []:
        '''функция поиска элементов заменяющая
        driver.find_element_by_
                                css_selector()
                                id()

        Поиск элементов по локатору на странице HTML 

        locator=(By.CSS_SELECTOR , selector)
        
        мой локатор имеет три аргеумнта
        'attribute': 'href', 
        'by': 'xpath', 
        'selector': ''
        --------------

        #if research: 
        research - опция исследования полученного элемента


        


        '''

        _driver_wait  :int = 1
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
    
    #@Log.logged 
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


    #@Log.logged 
    def page_refresh(self):
        '''Рефреш с ожиданием поной перезагрузки страницы
        '''
        self.driver.get_url(self.driver.current_url)
        pass
    
    #@Log.logged 
    def close(self):
        if self.driver.close(): self.print(''' DRIVER CLOSED ''')
        pass

    


    #@Log.logged 
    def researh_elements(self, elements)->bool:
        '''
        Функция для исследования элемента
        '''
        for element in elements:
            try:
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
                return True
            except:
                return False


