




###################################################################################################################################
#
#                                       
#                                          здесь собираются списки товаров от поставщиков
#    
#
####################################################################################################################################


import pandas as pd
import datetime
import time
import sys
from selenium.common.exceptions import *

import products
from ini_files import Ini
import execute_json as jsn
import check_and_convert_datatypes as check_type
from logger import Log
import products
from pathlib import Path

#@Log.logged
def execute_list_of_scenaries(self) -> bool :
    ''' по умолчанию все сценарии (имена файлов) прописаны в файе <supplier>.json 
    Каждый сценарий - файл с именем 
    <supplier_name>_categories_<category_name>_<model>_<brand>.json
    при инициализации объекта он хранится в self.scenaries
    
    self - class Supplier  f.e.: mor, cdata, visual, etc.
    '''
    ################################################################################


    # 0. 
    self.get_url(self.start_url)


    # 1.
    '''
                        если требуется логин на сайт
                        в классе поставщика вызываю сценарий log_in()
                        
    '''
    if self.required_login: 
        if not self.related_functions.log_in(self):return False


    # 2.
    '''
                        Запускаю каждый сценарий из из списка <supplier>.json["scenaries"]
    '''
    for scenario_files in self.scenaries:
        
        for json_file in scenario_files:      

            self.current_scenario = jsn.loads(self.ini_path/f'''{json_file}''')
            self.current_scenario_category = json_file.split('_')[2]
            
            run_scenario(self)

    return True


#@Log.logged
def run_scenario(self) -> bool:
    
    for scenario_node in self.current_scenario:
        '''
         -текущий сценарий исполнения состоит из узлов. Каждый узел состоит из:
        - <brand> 
        - [<model>] необязательное поле
        - <url> откуда собирать товары
        - <prestashop_category>
        - <price_rule> пересчет для магазина по умолчанию установливается в self.price_rule
        - <attributes> - свойства товара: цпу, экран, гарантия итп
        '''
        self.current_node = self.current_scenario[scenario_node]
        self.current_nodename = str(scenario_node)
        
        '''проверим значения всех атрибутов'''
        self.print_attr(self)
        build_products_list_by_scenario(self)
        
    '''
    если надо выкидывать каждый сценарий в файл
    '''
    #flush_p(self)



#@Log.logged
def build_products_list_by_scenario(self)->bool:
    '''
    все товары собираются в 
    список p[]
    каждый элемент списка это словарь с данными о товаре
    '''

    '''
                        1. собираю ссылки на товары со страниц категории, описанной узлом сценария
    
        
    '''
    list_urls_product_pages = soberi_list_urls_product_full_pages(self)



    '''                 2. Обрабатываю собранные результаты                             '''


    #а) Не получил страницу  {self.current_nodename["url"]} 
    if list_urls_product_pages == False or list_urls_product_pages == None or list_urls_product_pages == 'None' :
        self.print(f''' !!!!!  Не получил страницу  
        node
        {self.current_node}
        что-то пошло не так при сборе ссылок на страницы товаров 
        list_urls_product_pages = {list_urls_product_pages} 
        смотреть в сторону soberi_list_urls_product_full_pages_na_tovary_by_scenario_node
        ''')
        return self, False

    #б) Если вернулась строка - запаковавываю ее в список 
    #(так бывает, если по сценарию нашелся всего один товар )
    #elif str(type(list_urls_product_pages)).find('str') >-1 : 
    #    list_urls_product_pages : [] = [list_urls_product_pages]

    #в) Если пришел список 
    #else:pass
        #list_urls_product_pages = list(set(list_urls_product_pages)) 
        ''' при помощи set убираю дубликаты '''



    '''
                       3. По каждому URL строю prestashop товар
                       Релевантные каждому из поставщиков функции находятся в
                       suppliers.<suppler> и подлючаются через
                       self.related_functions.build_product(self)


    '''
    for product_url in list_urls_product_pages:
        self.get_url(product_url)
        self.related_functions.build_product(self)
        return self, True



#@Log.logged
def soberi_list_urls_product_full_pages(self) ->[]:
    '''  возвращает ссылки на все товары в категории 
        по локатору self.locators['product']['link_to_product_locator']
    '''
    try:
        ''' нет такой страницы! Возможно, проверить категорию в файле сценария ? '''
        if self.get_url(self.current_node["url"]) == False: 
            #self.print(f'''Ошибка перехода по адресу {self.category_url} 
            #Возможно, проверить категорию в файле сценария ? 
            #{self.current_scenario}''')
            return False , []
   
        #''' на странице категории могут находится  чекбоксы    
        # если их нет, в сценарии JSON они прописаны checkbox = false
        #'''
        json_checkboxes = self.current_node["checkbox"]
        if json_checkboxes: 
            click_checkboxes(self, json_checkboxes) 
            self.print(f''' есть чекбоксы {json_checkboxes}''')
       


        # Если я использую прокрутку вниз
        if self.locators['infinity_scroll'] == True: 
            scroller(self)
           

            list_product_urls = self.get_elements_by_locator(self.locators['product']['link_to_product_locator'])
            return list_product_urls


            # переключение между страницами
        else:
            list_product_urls :[]
            while click_to_next_page(self):
                list_product_urls += self.get_elements_by_locator(self, self.locators['product']['link_to_product_locator'])
                return list_product_urls

    except Exception as ex: 
        self.print(f'''Ошибка в функции 
        soberi_list_urls_product_full_pages(self)
        {ex}''')
        #sys.exit()
      


def scroller(self, wait=1 , prokrutok=5, scroll=500):
    '''
    Prokruka stranicy vniz
    '''
    try:
        for i in range(prokrutok):
            self.print(f'------------------------ Скроллинг вниз {i}--------------------------- ')
            self.driver.execute_script(f"window.scrollBy(0,{scroll})") # поднял окошко
            time.sleep(1)
            #self.wait(1)
        return True
    except Exception as ex:
        self.print(str(ex))
        return self, False
