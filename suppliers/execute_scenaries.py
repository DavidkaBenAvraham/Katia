

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



    # 2.
    '''
         Запускаю каждый сценарий из из списка <supplier>.json["scenaries"]
            файл сценариев Алиэкспресс отличается тем, что в файл включены хедеры
            магазинов. Я это сделал, чтобы не плодить мелкие файлы по 
            каждому магазину.
    '''
    def run(json_file):
        s.current_scenario = json.loads(Path(s.ini.paths.ini_files_dir , f'''{json_file}'''))
        s.current_scenario_category = json_file.split('_')[2]
        ''' третье слово в названии файла сценариев это категория товаров '''
        run_scenario(s)

    for scenario_files in s.supplier_settings_from_json["scenaries"]:
        ''' запускаю json файлы один за другим '''
        if str(type(scenario_files)).find('str')>-1:
            ''' если в сценарии есть всего один файл '''
            run(scenario_files)
        else:
            for json_file in [scenario_files]:
                run(json_file)

    return True

''' @print '''
def run_scenario(s) -> bool:
    '''
        -текущий сценарий исполнения состоит из узлов. Каждый узел состоит из:
    - <brand> 
    - [<model>] необязательное поле
    - <url> откуда собирать товары
    - <prestashop_category> список id категорий 
    - <price_rule> пересчет для магазина по умолчанию установливается в self.price_rule

    '''
    for scenario_node in s.current_scenario:

        def run():
            ''' бегунок '''

            '''      #########           1        ############# '''
            list_products_urls : list = get_list_products_urls(s)
            ''' получаю список url на страницы товаров '''
        


            if len(list_products_urls) == 0 : return False 
            ''' в исполняемом узле может не оказаться товаров.
                В таком случае перехожу к следующему узлу выполнения
            '''

        
            '''
             #       #########           2        ############# 
            '''
            for product_url in list_products_urls :
                ''' перебираю адреса товаров : '''


                #   a)
                s.driver.get_url(product_url)
                '''Перехожу на страницу товара '''

                #   b)
                #p_fields = s.related_functions.get_product_fields_from_product_page(s)
                ''' получаю поля товара '''

                #   c)
                s.p.append(products.Product().get_product_fields_from_product_page(s))
                ''' добавляю поля в список supplier.p[] '''


        s.dict_current_node = s.current_scenario[scenario_node]
        ''' текущий сценарий в формате dict '''

        if 'store_id' in s.dict_current_node:
            ''' 
            имеем дело с магазином
            текущий сценарий в формате dict сдвинут  вправо
            и находится в узле  scenaries 
            '''
            for scenario in s.dict_current_node['scenaries']:
                s.current_scenario = s.dict_current_node['scenaries'][scenario]
                s.current_node = s.dict_current_node['scenaries'][scenario]
              
                run()
            pass
           
        else:
            s.current_nodename = str(scenario_node)
            ''' имя узла сценария   '''
            run()




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

    page = s.related_functions.page(s = s)

    #''' на странице категории могут находится  чекбоксы    
    # если их нет, в сценарии JSON они прописаны checkbox = false
    #'''
    json_checkboxes = s.current_node["checkbox"]
    if json_checkboxes: 
        s.driver.click_checkboxes(s, json_checkboxes) 
        log.print(f''' есть чекбоксы {json_checkboxes}''')
       

    
    '''                     Существует два вида показа товаров: 
                            переключение между страницами и бесконечная прокрутка 
    '''
    if s.locators['infinity_scroll'] == True: 
        ''' А бесконечная прокрука '''
        s.driver.scroll()
        list_product_urls : list = s.driver.find(s.locators['product']['link_to_product_locator'])
        return list_product_urls
    
    else:
        ''' Б переключение между страницами'''

        list_product_urls : list = s.driver.find(s.locators['product']['link_to_product_locator'])
        ''' беру линки с певой страницы '''

        while page.click_to_next_page():
            ''' функция реализуется для каждого поставщика в зависимости от страницы '''
            list_product_urls += s.driver.find(s.locators['product']['link_to_product_locator'])
            ''' продолжаю собирать со след страниц '''


        return list_product_urls

