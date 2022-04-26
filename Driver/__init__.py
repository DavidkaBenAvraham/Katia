from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import os


from logger import Log
from ini_files import Ini

'''
##########################################
        опции запуска драйверов 
        google, Mozilla
        прописаны в файле
        driver_options
'''
import Driver.driver_options as driver_options
import execute_json as jsn

import pandas as pd
import datetime
import time


from attr import attrs, attrib, Factory
@attrs
class Driver(Log):
    driver : webdriver = attrib(init = False )
    current_url : str = attrib(init = False)
    '''
    Работа с вебдрайвером
    По умолчанию используется Firefox
    driver: имя драйвера (firefox, chrome, etc)
    wait: ожидание перед действиями селениума
    '''
    def __attrs_post_init__(self): 
        self.set_driver()
       
    #@Log.logged 
    def set_driver(self):      
        #_path_to_ini_file = f'''{self.root}\\Ini\\webdriver.json'''  
        #d = jsn.loads(_path_to_ini_file)["driver"]
        d = jsn.loads(self.ini_path / 'webdriver.json')["driver"]
        print(d["name"])
        #self.driver_wait = d['driver_wait']

        #try:



        #прячу браузер
        #os.environ['MOZ_HEADLESS'] = '1'

        '''
        новая версия создания драйвера
        '''
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
        #except Exception as ex: 
        #    self.print(f''' Ошибка запуска драйвера {ex} ''')
        #    return False























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
    def wait_to_be_clickable(self, locator, time_to_wait = 5):
        element_clickable = EC.element_to_be_clickable(locator)
        try:
            return WebDriverWait(self.driver , time_to_wait).until(element_clickable)
        except TimeoutException as ex:
            self.print(f''' не получила ответ от {element_clickable}  ''')
            self.log(ex)
            return False



    #@Log.logged 
    def get_url(self, url):
        '''
        переход по указанному урл
        '''
        try:

            self.driver.prev_url = self.driver.current_url
            self.driver.get(url)
            
            #WebDriverWait(driver, 10).until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')
            #self.log( f'''Страница загрузилась : {self.driver.current_url}''')
            return self, True
        except Exception as eх: 
            self.print(f''' 
            Ошибка {eх} 
            по адресу {url} ''' )
            return self,  False

    #@Log.logged 
    def find(self, locator):

        '''
        locator=(By.CSS_SELECTOR , selector)

        функция поиска элементов заменяющая
        driver.find_elements_by_css_selector()
        driver.find_element_by_css_selector()
        driver.find_elements_by_id()
        driver.find_element_by_id()
        find_element_by_
        --------------

        #if research: 
        research - опция исследования полученного элемента


        мой локатор имеет три аргеумнта
        'attribute': 'href', 'by': 'xpath', 'selector': ''

        убираю не релевантный
        '''
        
        



        try:  
            driver_wait  :int = 1
            # может вернуться или один или несколько элементов списком
            element = WebDriverWait(self.driver, int(driver_wait)).until(EC.presence_of_element_located((locator)))
            elements = WebDriverWait(self.driver, int(driver_wait)).until(EC.presence_of_all_elements_located((locator)))

        except NoSuchElementException as eх:
            self.print(f'''Exception NoSuchElementException:
            {eх}
            прекращаю поиск элемента {locator} , отдаю False''')
            return False
        except InvalidSessionIdException as e:
            self.print(f'''  - Потряна связь с сайтом !!!
            EXCEPTION InvalidSessionIdException: 
            {e}
            ''')
            self.driver.close()
            return False
        except StaleElementReferenceException as e: #
            self.print(f'''Exception StaleElementReferenceException:
            {e}
            прекращаю поиск элемента {locator} , отдаю False''')
            return False
        except InvalidArgumentException as e: #
            self.print(f'''Exception InvalidArgumentException:
            {e}
            прекращаю поиск элемента {locator} , отдаю False''')
            return False
        except TimeoutException as e: #
            self.print(f'''Exception TimeoutException:
            {e}
            прекращаю поиск элемента {locator} , отдаю False''')
            return False
        except ElementClickInterceptedException as e: 
            self.print(f'''Exception ElementClickInterceptedException:
            {e}
            прекращаю поиск элемента {locator} , отдаю False''')
            return False

        
        except Exception as e: 
            self.print(f'''  
            ОБЩАЯ ОШИБКА self.find() 
            Exception:
            {e}
            прекращаю поиск элемента {locator} , отдаю False''')
            return False

        else:
            '''
            Возвращает или СПИСОК
            элементов
            '''
            

            #   1) Если нашлось несколько
            if len(elements) >= 1: 
                return elements

            #   2) Если один строкой
            elif str(type(element)).find("webelement") >-1:
                return [element]
            
            #   3) ни одного
            else: return False
    
    #@Log.logged 
    def page_refresh(self):
        '''Рефреш с ожиданием поной перезагрузки страницы
        '''
        self.driver.get_url(self.driver.current_url)
        pass
    
    #@Log.logged 
    def close(self):
        
        if self.driver.close(): self.log(''' DRIVER CLOSED ''')
        pass

    #@Log.logged 
    def researh_elements(self, elements):
        '''
        Функция для исследования элемента
        '''
        for element in elements:
            try:
                '''
                Исследование силами Селениума
                '''
                log_str = str(f'''
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
                ''')
            
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

                log_str += str(f'''
                Javascript:
                -----------------------------------------
                {attrs} \n
                ''')
                self.log(log_str)
            except:
                return False







    #@Log.logged
    def get_elements_by_locator(self, locator) ->[]:

        '''
        возвращает список значений аттрибута элементов найденных по локатору <locator>
        
        locator содержит три элемента:

                - "attribute": "sendKeys(Keys.RETURN)", 
                    использую обработку полученного элемента
                            Примеры аттрибутов:
                    - href
                    - a
                    - text
                    - innerHTML
                    - innerText
                    - sendKeys(Keys.RETURN)



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




        etc.
        '''
        out = []


        elements = self.find( (locator['by'],locator['selector']))

        '''

            elements 
            может получить список элементов или один элемент или хуй

            Функция  возвращает список [] или False


        '''
        if elements == False:return False

        if str(type(elements)).find("class 'list'") >-1:
            '''если нашлось несколько 
            элементов по указанному локатору '''
                
            for element in elements:
                try: out.append(str(element.get_attribute(locator['attribute'])))
                except StaleElementReferenceException as e:
                    self.print(f'''ElementClickInterceptedException - \n  {e} \n
                    потеряна связь с DOM {locator}''')
                    continue
            return out
        elif str(type(elements)).find("WebElement") >-1: 
            '''
            если нашелся только один
            '''
            out.append(elements.get_attribute(locator['attribute']))
            return out