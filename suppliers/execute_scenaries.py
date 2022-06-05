

###################################################################################################################################
#
#                                       
#                                          здесь собираются списки товаров от поставщиков
#    
#
####################################################################################################################################


from logging import log
import pandas as pd
import datetime
import time
import sys
from pathlib import Path

from ini_files_dir import Ini
import execute_json as json
from logger import Log
import products
from strings_formatter import StringFormatter as SF

''' @print '''
def execute_list_of_scenaries(Supplier) -> bool :
    ''' по умолчанию все сценарии (имена файлов) прописаны в файе <supplier>.json 
    Каждый сценарий - файл с именем 
    <supplier>_categories_<category_name>_<model>_<brand>.json
    при инициализации объекта он хранится в self.scenaries
    
    supplier - class Supplier  f.e.: mor, cdata, visual, etc.

    '''
    ################################################################################

    s = Supplier
    #^^^^^^^^^^^^
    '''
       s - значит Supplier

    '''


    # 0. 
    if not s.driver.get_url(s.supplier_settings_from_json['start_url']):
        print(f''' supplier not started in url:
       {s.supplier_settings_from_json['start_url']}''')
        return False



    # 1.
    '''
                        если требуется логин на сайт
                        в классе поставщика вызываю сценарий log_in()            
    '''
    if s.if_login: 
        if not s.related_functions.log_in():
            return False ,  print(f''' 
            supplier not logged in on: 
            {s.driver.current_url}''')


    # 2.
    '''

   
         Запускаю каждый сценарий из из списка <supplier>.json["scenaries"]
    '''
    for scenario_files in s.supplier_settings_from_json["scenaries"]:
        
        for json_file in scenario_files:      

            s.current_scenario = json.loads(Path(s.ini.paths.ini_files_dir , f'''{json_file}'''))
            s.current_scenario_category = json_file.split('_')[2]
            run_scenario(s)

    return True

''' @print '''
def run_scenario(s) -> bool:
    for scenario_node in s.current_scenario:
        '''
         -текущий сценарий исполнения состоит из узлов. Каждый узел состоит из:
        - <brand> 
        - [<model>] необязательное поле
        - <url> откуда собирать товары
        - <prestashop_category> список id категорий 
        - <price_rule> пересчет для магазина по умолчанию установливается в self.price_rule
        - <attributes> - свойства товара: цпу, экран, гарантия итп
        '''


        s.current_node = s.current_scenario[scenario_node]
        ''' текущий сценарий в формате dict '''
        s.current_nodename = str(scenario_node)
        ''' имя узла сценария '''
        

        '''
        '''      #########           1        ############# 
        list_products_urls : list = get_list_products_urls(s)
        ''' получаю список url на страницы товаров '''
        
        if len(list_products_urls) == 0 : continue 
        ''' в исполняемом узле может не оказаться товаров.
            В таком случае перехожу к следующему узлу выполнения
        '''

        
        '''
         #       #########           2        ############# 
        '''
        for product_url in list_products_urls :
            ''' перебираю адреса товаров '''
            s.driver.get_url(product_url)
            '''Перехожу на страницу товара '''

            p_fields = s.related_functions.get_product_fields_from_product_page(s)
            ''' получаю поля товара '''

            s.p.append(p_fields)
            ''' добавляю поля в список supplier.p[] '''

        return True

#@print
def get_list_products_urls(s) ->list:
    '''  возвращает ссылки на все товары в категории 
        по локатору self.locators['product']['link_to_product_locator']
    '''
    
        
    if not s.driver.get_url(s.current_node["url"]): 
        return [] , log.print(f'''нет такой страницы! 
                {s.current_node["url"]}
                Возможно, 
                проверить категорию в файле сценария ? ''')



    #''' на странице категории могут находится  чекбоксы    
    # если их нет, в сценарии JSON они прописаны checkbox = false
    #'''
    json_checkboxes = s.current_node["checkbox"]
    if json_checkboxes: 
        s.driver.click_checkboxes(s, json_checkboxes) 
        log.print(f''' есть чекбоксы {json_checkboxes}''')
       

    
    '''     Существует два вида показа товаров: 
    переключение между страницами и бесконечная прокрука 
    
    '''

    if s.locators['infinity_scroll'] == True: 
        ''' бесконечная прокрука '''
        s.driver.scroll()
        list_product_urls : list = s.driver.find(s.locators['product']['link_to_product_locator'])
        return list_product_urls
    
    else:
        '''переключение между страницами'''
        list_product_urls : list
        while click_to_next_page(s):
            list_product_urls += s.driver.find(s.locators['product']['link_to_product_locator'])
            return list_product_urls


