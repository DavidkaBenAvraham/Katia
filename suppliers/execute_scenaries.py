

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
from strings_formatter import StringFormatter 

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
    _d = s.driver
   


    # 0. 
    if not _d.get_url(s.supplier_settings_from_json['start_url']):
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

        if isinstance(scenario_files, str):
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
    while len(s.current_scenario.items())>0:
        node = s.current_scenario.popitem()[1]
        ''' 
        иду по именам узлов сценария 
        если поставщик это алиэкспресс, то это магазины поставщика
        в таком файле  сценарий в формате  сдвинут  вправо в scenaries{}
        я его отличаю по признаку store_id
        если поставщик это ksp, то это узлы категорий

        '''


        def run(s):
            ''' бегунок '''

            '''      #########           1        ############# '''
            list_products_urls : list = get_list_products_urls(s , node)
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
                product : dict = s.related_functions.grab_product_page(s)
                ''' получаю поля товара '''

                #   c)
                
                s.p.append(product)
                ''' добавляю поля в список supplier.p[] '''


        if 'store_id' in s.current_scenario:
            ''' 
            имеем дело с магазином
            текущий сценарий в формате dict сдвинут  вправо
            и находится в узле  scenaries:{}
            '''
            for scenario in s.dict_current_node['scenaries']:
                s.current_scenario = s.dict_current_node['scenaries'][scenario]
                for scenario_node in s.dict_current_node['scenaries'][scenario].items():
                    s.current_node = scenario_node
                    run(s)
            pass
           
        else:
            ''' имею дело с узлом сценария как в ksp, mor, etc '''
            run(s)




        return True

#@print
def get_list_products_urls(s , scenario_node : dict ) ->list:
    '''  возвращает ссылки на все товары в категории 
        по локатору self.locators['product']['link_to_product_locator']
    '''
    
    if not s.driver.get_url(scenario_node["url"]): 
        return [] , log.print(f'''нет такой страницы! 
                {s.current_node["url"]}
                Возможно, 
                проверить категорию в файле сценария ? ''')
    

    #''' на странице категории могут находится  чекбоксы    
    # если их нет, в сценарии JSON они прописаны checkbox = false
    #'''
    json_checkboxes = scenario_node["checkbox"]
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

        paginator = s.driver.find(s.locators['pagination_block'])
        list_product_urls : list = []
        def pagination(list_product_urls):
            list_product_urls += s.driver.find(s.locators['product']['link_to_product_locator'])
            ''' беру линки с страницы '''

            if len(paginator)>0:
                pagination()
                pass

        pagination(list_product_urls)

        return list_product_urls



