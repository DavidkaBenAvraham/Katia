# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia.Supplier
##Documentation for this module
#                                       
#    здесь собираются списки товаров от поставщиков



from pathlib import Path
import execute_json as json


def execute_list_of_scenaries(Supplier) -> bool :
    ## по умолчанию все сценарии  прописаны в файлах <supplier>.json
    # Каждый сценарий поставщика - файл с именем 
    # <supplier>_categories_<category_name>_<model>_<brand>.json
    # при инициализации объекта он хранится в self.scenaries
    # -------------------------------
    # supplier - class Supplier  f.e.: mor, cdata, visual, etc.


    s = Supplier
    _d = s.driver
   
    
    ## 0. 
    if not _d.get_url(s.settings['start_url']):
        print(f''' supplier not started in url:
       {s.settings['start_url']}''')
        return False



    ## 1.
        # Запускаю каждый сценарий из из списка <supplier>.json["scenaries"]
        #   файл сценариев Алиэкспресс отличается тем, что в файл включены хедеры
        #   магазинов. Я это сделал, чтобы не плодить мелкие файлы по 
        #   каждому магазину.
    def run(json_file) -> bool:
        s.scenaries = json.loads(Path(s.ini.paths.ini_files_dir , f'''{json_file}'''))
        s.scenario_category = json_file.split('_')[2]
        ''' третье слово в названии файла сценариев это категория товаров '''
        while len(s.scenaries.items())>0:
            _scenario = s.scenaries.popitem()[1]
            try : 
                run_scenario(s , _scenario) 
                return True
            except Exception as ex:
                print(f''' ошибка {ex} в ходе выполнения сценария {json_file} ''')
                return False
            
        

    for scenario_files in s.settings["scenaries"]:
        ''' запускаю json файлы один за другим '''

        if isinstance(scenario_files, str):
            ''' если в сценарии есть всего один файл '''
            run(scenario_files)
        else:
            for json_file in [scenario_files]: 
                run(json_file)
               

    return True


def run_scenario(s , scenario) -> bool:
    '''
    -текущий сценарий исполнения состоит из узлов. Каждый узел состоит из:
    - <brand> 
    - [<model>] необязательное поле
    - <url> откуда собирать товары
    - <prestashop_category> список id категорий 
    - <price_rule> пересчет для магазина по умолчанию установливается в self.price_rule

    '''
    

    def run(s, node):
        ''' бегунок '''

        ## 1)
        list_products_urls : list = get_list_products_urls(s , node)
        ''' получаю список url на страницы товаров '''

        if len(list_products_urls) == 0 : return False 
        ## в исполняемом узле может не оказаться товаров. В этом случае перехожу к следующему узлу выполнения

        ## 2)
        for product_url in list_products_urls :
            ''' перебираю адреса товаров : '''


            #   a)
            if not s.driver.get_url(product_url) : 
                '''Перехожу на страницу товара 
                    функция get_url('url') возвращает True, 
                    если переход на страницу был успешен'''

                print(f''' нет такой страницы товара {product_url} ''') 
                continue
                

            try:

                #   b)
                product = s.related_functions.grab_product_page(s)
                ''' получаю товар '''
                

                #   c)
                s.p.append(product)
                ''' добавляю товар в список supplier.p[] '''
            except Exception as ex: 
                print(f''' Ошибка {ex} при сборе товара со страницы {product_url} ''')
                continue

    if 'store_id' in scenario.keys():
        ##         имеем дело с магазином
        # текущий сценарий в формате dict сдвинут  вправо 
        # и находится в узле  scenaries:{} 
        while len(scenario['scenaries'].items())>0:
            run(s , scenario['scenaries'].popitem()[1])
    else:
        ''' имею дело с узлом сценария как в ksp, mor, etc '''
        run(s , scenario)
    return True


def get_list_products_urls(s , scenario_node : dict ) ->list:
    '''  возвращает ссылки на все товары в категории 
        по локатору self.locators['product']['link_to_product_locator']
    '''
    
    if not s.driver.get_url(scenario_node["url"]): 
        return [] , log.print(f'''нет такой страницы! 
                {s.current_node["url"]}
                Возможно, 
                проверить категорию в файле сценария ? ''')
    

    ##''' на странице категории могут находится  чекбоксы    
    ## если их нет, в сценарии JSON они прописаны checkbox = false
    ##'''
    #json_checkboxes = scenario_node["checkbox"]
    #if json_checkboxes: 
    #    s.driver.click_checkboxes(s, json_checkboxes) 
    #    log.print(f''' есть чекбоксы {json_checkboxes}''')
       

    


    ##                     Существует два вида показа товаров: 
    #                      переключение между страницами и бесконечная прокрутка 
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



