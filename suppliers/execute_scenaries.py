

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
from pathlib import Path

from ini_files_dir import Ini
import execute_json as json
from logger import Log
import products
from formatter import Formatter
formatter = Formatter()

@Log.log
def execute_list_of_scenaries(self) -> bool :
    ''' по умолчанию все сценарии (имена файлов) прописаны в файе <supplier>.json 
    Каждый сценарий - файл с именем 
    <supplier>_categories_<category_name>_<model>_<brand>.json
    при инициализации объекта он хранится в self.scenaries
    
    self - class Supplier  f.e.: mor, cdata, visual, etc.
    '''
    ################################################################################


    # 0. 
    page_source = self.get_url(self.supplier_settings_dict['start_url'])



    # 1.
    '''
                        если требуется логин на сайт
                        в классе поставщика вызываю сценарий log_in()
                        
    '''
    if self.if_login: 
        if not self.related_functions.log_in(self):return False


    # 2.
    '''

   
                        Запускаю каждый сценарий из из списка <supplier>.json["scenaries"]


    '''
    for scenario_files in self.scenaries:
        
        for json_file in scenario_files:      

            self.current_scenario = json.loads(Path(self.ini.paths.ini_files_dir , f'''{json_file}'''))
            self.current_scenario_category = json_file.split('_')[2]
            run_scenario(self)

    return True


@Log.log
def run_scenario(self) -> bool:
    
    for scenario_node in self.current_scenario:
        '''
         -текущий сценарий исполнения состоит из узлов. Каждый узел состоит из:
        - <brand> 
        - [<model>] необязательное поле
        - <url> откуда собирать товары
        - <prestashop_category> список id категорий 
        - <price_rule> пересчет для магазина по умолчанию установливается в self.price_rule
        - <attributes> - свойства товара: цпу, экран, гарантия итп
        '''


        self.current_node = self.current_scenario[scenario_node]
        ''' текущий сценарий в формате dict '''
        self.current_nodename = str(scenario_node)
        ''' имя узла сценария '''
        

        '''
        '''      #########           1        ############# 
        urls = get_list_products_urls(self)
        ''' получаю список url на страницы товаров '''


        
        
        if urls == None : continue 
        ''' в категории может не оказаться товаров.
            Если не получил  url страниц товара перехожу 
           в следующую по сценарию категорию
        '''

        
        '''
         #       #########           2        ############# 
        '''
        for product_url in urls :
            ''' перебираю адреса товаров '''

            self.get_url(product_url)
            '''Перехожу на страницу товара '''

            p_fields = self.related_functions.get_product_fields(self)
            ''' получаю поля товара '''

            self.p.append(p_fields)
            ''' добавляю поля в список для экспорта полей '''

        return True

@Log.log
def get_list_products_urls(self) ->[]:
    '''  возвращает ссылки на все товары в категории 
        по локатору self.locators['product']['link_to_product_locator']
    '''

        
    if self.get_url(self.current_node["url"]) == False : 
        ''' нет такой страницы! Возможно, проверить категорию в файле сценария ? '''
        return False 



    #''' на странице категории могут находится  чекбоксы    
    # если их нет, в сценарии JSON они прописаны checkbox = false
    #'''
    json_checkboxes = self.current_node["checkbox"]
    if json_checkboxes: 
        click_checkboxes(self, json_checkboxes) 
        self.print(f''' есть чекбоксы {json_checkboxes}''')
       

    
    '''     Существует два вида показа товаров: 
    переключение между страницами и бесконечная прокрука 
    
    '''

    if self.locators['infinity_scroll'] == True: 
        ''' бесконечная прокрука '''
        scroller(self)
           
        list_product_urls = self.find(self.locators['product']['link_to_product_locator'])
        ''' self.find() = .find_by(by, selector) 
            by = XPATH | ID | CSS_SELECTOR etc.
            см. webdrivers.__init__.py
        '''
        return list_product_urls
    
    else:
        '''переключение между страницами'''
        list_product_urls : list
        while click_to_next_page(self):
            list_product_urls += self.find(self.locators['product']['link_to_product_locator'])
            return list_product_urls

@Log.log
def scroller(self, wait=1 , prokrutok=5, scroll=500):
    '''
    Prokruka stranicy vniz
    '''
    try:
        for i in range(prokrutok):
            #self.print(f'------------------------ Скроллинг вниз {i}--------------------------- ')
            self.driver.execute_script(f"window.scrollBy(0,{scroll})") # поднял окошко
            time.sleep(1)
            #self.wait(1)
        return True
    except Exception as ex:
        self.print(str(ex))
        return self, False
