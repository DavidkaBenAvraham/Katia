from typing import List
import execute_json as json
from pathlib import Path
import pandas as pd
from attr import attrib, attrs, Factory
from selenium.webdriver.remote.webelement import WebElement 
from strings_formatter import StringFormatter



sf = StringFormatter()
shops : list = []

def login(s) -> bool :

    pass
    locators =  s.locators['login']

    try:
        ''' всякие банннеры '''
        s.driver.find(locators['close banner'])[0].click()
        s.driver.find(locators['open_login_popup_button'])[0].click()
        s.driver.find(locators['open_login_popup_button']['open_login_popup_button 2lvl'])[0].click()

    except Exception as ex: return False, print(ex)


    try:
        s.driver.find(locators['user_locator'])[0].send_keys( locators['user'])
        s.driver.find(locators['password_locator'])[0].send_keys( locators['password'])
        s.driver.find(locators['send_locator'])[0].click()
    except Exception as ex:return False, print(ex)

''' ------------------ НАЧАЛО -------------------------- '''
stores:list = []
def run_shops(s):
    
    stores_groups_files_dict = json.loads(Path(s.ini.paths.ini_files_dir , f'''aliexpress.json'''))['scenaries']
    for stores_group_file in stores_groups_files_dict:
        stores_dict = json.loads(Path(s.ini.paths.ini_files_dir , f'''{stores_group_file}'''))
        try:
            for store_settings_dict in stores_dict.items(): 
                stores.append({
                'store ID': store_settings_dict[1]['store_id'] ,
                'pail': 1,
                'store description': store_settings_dict[1]['description'],
                'parent category': 3,
                'root': 0 ,
                'aliexpress_url' : store_settings_dict[1]['shop_url'],
                'store_categories_ajax': store_settings_dict[1]['ajax_shop_file']
                })


                run_local_scenario(s,stores[-1])
                '''запускаю последний добавленный в список '''

        except Exception as ex:return False, print(ex)
    pass 
    ''' ------------------ КОНЕЦ  -------------------------- '''

def get_ajax_from_store(s , store_settings_dict : dict = {}) -> dict:
    s.driver.get_url(store_settings_dict['store_categories_ajax'] )
    ajax_from_store = s.driver.find(s.locators['store']['data_from_store_ajax_file'])[0].text
    return ajax_from_store


''' ------------------ НАЧАЛО -------------------------- ''' 
def build_shop_categories(s , store_settings_dict : dict) -> dict:   

   
    s.driver.get_url(store_settings_dict[1]['all-wholesale-products'])
    #try:
    #    s.driver.find(s.locators['eng version'])[0].click()
    #except Exception as ex : print(ex)
    
    if s.driver.current_url != store_settings_dict[1]['all-wholesale-products']:
        if str(s.driver.current_url).find('login.aliexpress')>0:login(s)
        else:print(s.driver.current_url)
        s.driver.get_url(store_settings_dict[1]['all-wholesale-products'])
        pass


    categoties_blocks_html = s.driver.find(s.locators['store']['sub_block_main_item'])[0]
    elements = categoties_blocks_html.find_elements_by_xpath("//*[@class='group-item']")
    
    for  el in elements:
        main_category = el.find_elements_by_tag_name("a")[0]
        main_category_name = main_category.get_attribute('text')
        main_category_url = main_category.get_attribute('href')
        main_category_url_list = main_category_url.split('/')[-1].split('.')[0].split('_')
        main_category_id = main_category_url_list[-1]
        shop_id = main_category_url_list[0]
        t.append({
                'category ID': main_category_id ,
                'pail': 1,
                'category name': main_category_name,
                'parent category': shop_id,
                'root': 0 ,
                'aliexpress_url' : main_category_url
                })

        sub_blocks = el.find_elements_by_tag_name("ul")
        if len(sub_blocks)>0: 
            subs = sub_blocks[0].find_elements_by_tag_name("a")
            for sub in subs:
                sub_category_name = sub.get_attribute('text')
                sub_category_url = sub.get_attribute('href')
                sub_category_url_list = sub_category_url.split('/')[-1].split('.')[0].split('_')
                sub_category_id = sub_category_url_list[-1]
                shop_id = sub_category_url_list[0]
                t.append({
                    'category ID': sub_category_id ,
                    'pail': 1,
                    'category name': sub_category_name,
                    'parent category': main_category_id,
                    'root': 0 ,
                    'aliexpress_url' : sub_category_url
                    })
                
    
    s.export(data = t , format = ['csv'] )
    pass
    ''' ------------------ КОНЕЦ  -------------------------- '''

def run_local_scenario(s, store_settings_dict: dict = {}):
    ajax_from_store = get_ajax_from_store(s, store_settings_dict)
    #ajax_from_store = sf.remove_HTML_tags(ajax_from_store)
    s.export(ajax_from_store , ['json'] , store_settings_dict['store ID'])
    print(f''' {store_settings_dict['store ID']} added''')


''' ------------------ НАЧАЛО -------------------------- '''
@attrs
class page: 
    paginator : WebElement = attrib(init = False , default = None)
    ''' paginator - объект листатель '''

    s : object = attrib(kw_only = True, default = None)     
    ''' object Supplier '''


    def set_paginator(self):
        ''' object Supplier '''
        self.paginator = self.s.driver.find(self.s.locators['pagination_block'])
        pass

    def __attrs_post_init__(self, *args, **kwards):
        self.set_paginator()
        pass

    def click_to_next_page(self) -> bool:
        #self._s
        pass

    def get_product_fields_from_product_page(s):
        pass

products: list = []




