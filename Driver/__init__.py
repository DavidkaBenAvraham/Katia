from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import os


from Logging import Log as Log
from Ini import Ini

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




class Driver(Log):
    '''
    Работа с вебдрайвером
    По умолчанию используется Firefox
    driver: имя драйвера (firefox, chrome, etc)
    wait: ожидание перед действиями селениума
    '''
    def __init__(self, **kwards): 
         
        super().__init__(**kwards)
        
        self.set_driver(**kwards)
       
    @Log.log_f 
    def set_driver(self ,**kwards):      
        _path_to_ini_file = f'''{self.path_root}/Ini/webdriver.json'''  
        _driver_name = jsn.loads(_path_to_ini_file)["driver"]
        self.driver_wait = jsn.loads(_path_to_ini_file)["driver_wait"]

        #try:



        #прячу браузер
        #os.environ['MOZ_HEADLESS'] = '1'

        '''
        новая версия создания драйвера
        '''
        if _driver_name == 'chromedriver': 
            chrome_options = webdriver.ChromeOptions()
            for argument in jsn.loads(_path_to_ini_file)["arguments"]:
                    chrome_options.add_argument(argument)
            self.driver = webdriver.Chrome(options = chrome_options)
            
        if _driver_name == 'firefox': self.driver = webdriver.Firefox(options = driver_options.firefox_options(self))  
        if _driver_name == 'opera': self.driver = webdriver.Opera(options = driver_options.opera_options(self))
        if _driver_name == 'edge': self.driver = webdriver.Edge(options = driver_options.edge_options(self))
        self.driver.maximize_window()
        return self.driver

        #except Exception as ex: 
        #    self.log(f''' Ошибка запуска драйвера {ex} ''')
        #    return False

    #def driver(self):
    #    return self.driver
    @Log.log_f 
    def driver_implicity_wait(self , wait):
        '''
        Неявное ожидание указывает WebDriver'у опрашивать DOM определенное количество времени, 
        когда пытается найти элемент или элементы, которые недоступны в тот момент. 
        Значение по умолчанию равно 0. После установки, неявное ожидание устанавливается 
        для жизни экземпляра WebDriver объекта.
        #self.wait = WebDriverWait(self.driver, kwargs.get('wait')) if 'wait' in kwargs else WebDriverWait(self.driver, 20)
        '''
        self.driver.implicitly_wait(wait)
        
    @Log.log_f    
    def wait(self , wait_in_seconds):
        '''
        Явное ожидание
        лучше чем time.sleep()
        '''
        WebDriverWait(self.driver, wait_in_seconds)
        time.sleep(wait_in_seconds)
    @Log.log_f 
    def wait_to_precence_located(self, element_locator):
        '''
        locator=(By.CSS_SELECTOR , selector)
        '''
        self.log(f''' Ждём локатор {element_locator} ''')
        element_precence_located = EC.presence_of_element_located(element_locator)
        return element_precence_located
        pass

    @Log.log_f 
    def click(self, element_locator):
        element = self.wait_to_be_clickable(element_locator)
        if element == Falsex:
            element = self.find(element_locator)
            if element == Falsex:
                self.log(f''' Не нажался элемент {element_locator} ''')
                return False
            try: element.click()
            except : 
                self.log(f''' Не нажался элемент {element_locator} ''')
                return False
    @Log.log_f 
    def wait_to_be_clickable(self, element_locator, time_to_wait = 5):
        element_clickable = EC.element_to_be_clickable(element_locator)
        try:
            return WebDriverWait(self.driver , time_to_wait).until(element_clickable)
        except TimeoutException as ex:
            self.log(f''' не получила ответ от {element_clickable}  ''')
            self.log(ex)
            return False

    #@Log.log_f 
    def get_listattributes_from_allfound_elements(self , attribute , element_locator,  research = False):
        '''
        возвращает список значений аттрибута элементов найденных по локатору <element_locator>
        или одно значение одного элемена, найденного по его локатору.
        Примеры аттрибутов:
        - href
        - a
        - text
        - innerHTML
        - innerText
        etc.
        '''
        out = []
        try:
            elements = self.find(element_locator,  research)
            #self.log( str(f'''Найдены элелменты {elements} '''))
            ##self.screenshot(log_str)
            if str(type(elements)).find("class 'list'") >-1:  # Если появилось несколько
                '''если нашлось несколько 
                элементов по указанному локатору '''
                
                for element in elements:
                    try: out.append(str(element.get_attribute(attribute)))
                    except StaleElementReferenceException as ex:
                        self.log(f'''ElementClickInterceptedException - \n  {ex} \n
                        потеряна связь с DOM {element_locator}''')
                return out
            elif str(type(elements)).find("WebElement") >-1:  # нашелся только один элемент
                '''
                если нашелся только один
                '''
                out.append(elements.get_attribute(attribute))
                return out
                #self.log(f'''get_listattributes_from_allfound_elements out:{out}''')
                #return out
        except Exception as ex:
            self.log(f''' Упс {ex} ''')
            self.driver.close()
            return False
        

    @Log.log_f 
    def get_attribute_from_first_found_element(self , attribute , element_locator,  research = False):     
        ''' по локаторы вытаскиваю из элемента атрибуты:
        innerHTML, text, href etc. '''
        try:
            elements = self.find(element_locator,  research)
            if str(type(elements)).find("class 'list'") >-1:  # Если появилось несколько
                # беру первый
                for element in elements:
                    out = str(element.get_attribute(attribute))
                    return out
                    break
            elif str(type(elements)).find("webelement") >-1:  # нашелся только один элемент
                out = str(elements.get_attribute(attribute))
                return out
        except Exception as ex: 
            self.log(ex)
            self.log(f"Не нашел элемент по локатору {element_locator}")
            return False



    @Log.log_f 
    def get_url(self, url , **kwards):
        '''
        переход по указанному урл
        '''
        try:
            try:
                self.driver.prev_url = self.driver.current_url
            except: pass
            
            self.driver.get(url)
            
            #WebDriverWait(driver, 10).until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')
            self.log( f'''Страница загрузилась : {self.driver.current_url}''')
            return True
        except Exception as ex: 
            self.log(str(f''' 
            Ошибка {ex} 
            по адресу {url} ''' ))
            return False

    #@Log.log_f 
    def find(self, element_locator,  research = True) -> []:

        '''
        locator=(By.CSS_SELECTOR , selector)

        функция поиска элементов заменяющая
        driver.find_elements_by_css_selector()
        driver.find_element_by_css_selector()
        driver.find_elements_by_id()
        driver.find_element_by_id()
        find_element_by_
        --------------
        research - опция исследования полученного элемента
        '''
        
        #if research: self.log(f''' research включён! будет много инфо! ''')
        try:  

            # может вернуться или один или несколько элементов списком
            element = WebDriverWait(self.driver, int(self.driver_wait)).until(EC.presence_of_element_located((element_locator)))
            elements = WebDriverWait(self.driver, int(self.driver_wait)).until(EC.presence_of_all_elements_located((element_locator)))

        except NoSuchElementException as ex:
            self.log(f'''Exception NoSuchElementException:
            {ex}
            прекращаю поиск элемента {element_locator} , отдаю False''')
            return False,ex
        except InvalidSessionIdException as ex:
            self.log(f'''  - Потряна связь с сайтом !!!
            EXCEPTION InvalidSessionIdException: 
            {ex}
            ''')
            self.driver.close()
            return False,ex
        except StaleElementReferenceException as ex: #
            self.log(f'''Exception StaleElementReferenceException:
            {ex}
            прекращаю поиск элемента {element_locator} , отдаю False''')
            return False,ex
        except InvalidArgumentException as ex: #
            self.log(f'''Exception InvalidArgumentException:
            {ex}
            прекращаю поиск элемента {element_locator} , отдаю False''')
            return False,ex
        except TimeoutException as ex: #
            self.log(f'''Exception TimeoutException:
            {ex}
            прекращаю поиск элемента {element_locator} , отдаю False''')
            return False,ex
        except ElementClickInterceptedException as ex: 
            self.log(f'''Exception ElementClickInterceptedException:
            {ex}
            прекращаю поиск элемента {element_locator} , отдаю False''')
            return False,ex

        
        except Exception as ex: 
            self.log(f''' ОБЩАЯ ОШИБКА self.find() ''')
            self.log(f'''Exception Exception:
            {ex}
            прекращаю поиск элемента {element_locator} , отдаю False''')
            return False,ex

        else:
            '''
            Возвращает или СПИСОК
            элементов
            '''
            

            #1) Если нашлось несколько
            if len(elements) > 1: 
                #self.log(f'''Нашлось   {len(elements)}   элементов''')
                if research: self.researh_elements(elements)
                return elements
            #2) Если один из списка            
            if len(elements) == 1: 
                #self.log(f'''Нашлось   {len(elements)}   элементов''')
                if research: self.researh_elements(elements)
                return elements[0]
            #2) Если один 
            elif str(type(element)).find("webelement") >-1:
                    #self.log(f'''Нашелся ( 1 ) элемент''')
                    if research: self.researh_elements(element)
                    return [element]
            #3) ни одного
            else: return False
    
    @Log.log_f 
    def page_refresh(self):
        '''Рефреш с ожиданием поной перезагрузки страницы
        '''
        self.driver.get_url(self.driver.current_url)
        pass
    
    @Log.log_f 
    def close(self):
        
        if self.driver.close(): self.log(''' DRIVER CLOSED ''')
        pass

    @Log.log_f 
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

