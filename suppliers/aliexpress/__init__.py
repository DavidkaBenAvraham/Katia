from typing import List
import execute_json as json
from pathlib import Path
import pandas as pd
from attr import attrib, attrs, Factory
from selenium.webdriver.remote.webelement import WebElement 

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
t:list = []
def run_shops(s):
    
    shops_groups_files_dict = json.loads(Path(s.ini.paths.ini_files_dir , f'''aliexpress.json'''))['shops']
    for shop_group_file in shops_groups_files_dict:
        shops_dict = json.loads(Path(s.ini.paths.ini_files_dir , f'''{shop_group_file}'''))
        try:
            for shop_dict in shops_dict.items(): 
                t.append({
                'category ID': shop_dict[1]['store_id'] ,
                'pail': 1,
                'category name': shop_dict[1]['description'],
                'parent category': 3,
                'root': 0 ,
                'aliexpress_url' : shop_dict[1]['shop_url']
                })

                build_shop_categories(s , shop_dict)
        except Exception as ex:return False, print(ex)
    pass 
    ''' ------------------ КОНЕЦ  -------------------------- '''



''' ------------------ НАЧАЛО -------------------------- ''' 
def build_shop_categories(s , shop_dict : dict) -> dict:   

   
    s.driver.get_url(shop_dict[1]['all-wholesale-products'])
    #try:
    #    s.driver.find(s.locators['eng version'])[0].click()
    #except Exception as ex : print(ex)
    
    if s.driver.current_url != shop_dict[1]['all-wholesale-products']:
        if str(s.driver.current_url).find('login.aliexpress')>0:login(s)
        else:print(s.driver.current_url)
        s.driver.get_url(shop_dict[1]['all-wholesale-products'])
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


''' ------------------ НАЧАЛО -------------------------- '''
@attrs
class page: 
    paginator : WebElement = attrib(init = False , default = None)
    ''' paginator - объект листатель '''

    s : object = attrib(kw_only = True, default = None)     
    ''' object Supplier '''


    def set_paginator(self):
        ''' object Supplier '''
        self.paginator = s.driver.find(s.locators['pagination_block'])
        pass

    def __attrs_post_init__(self, *args, **kwards):
        self.set_paginator()
        pass

    def click_to_next_page(self) -> bool:
        #self._s
        pass



''' ------------------ НАЧАЛО -------------------------- ''' 
@attrs
class categories:

    _aliexpress_root_category : int = attrib(init = False , default = 3)
    _category_url : str = attrib(init = False , default = None)
    t : Factory(list) = attrib(init = False , default = None)
    _parent_category : int = attrib(init=False, default = None)  

    def __attrs_post_init__(self, *args, **kwards):
        self._aliexpress_root_category : int = attrib(init = False , default = 3)
        self._category_url = 'https://www.aliexpress.com/all-wholesale-products.html'
        self.t = []
        self.t.append(
                        {'category ID': 3 ,
                    'pail': 1,
                    'category name': 'ALIEXPRESS',
                    'parent category': 2,
                    'root': 0 ,
                    'category_url' : 'https://www.aliexpress.com/all-wholesale-products.html'}
                              )
        ''' первая строка таблицы '''
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- ''' 
    def fill_categories_table(self , s, html_block : dict = {} ,  parent_category : int = 3) -> bool:
        ''' parent_category : откуда строится дерево 
            3 : root для алиэкспресс в моем (e-cat.me) дереве категорий 
        '''

        
        for item in html_block:
                text = item.get_attribute('text')
                href = item.get_attribute('href')
                _vlst = href.split('/')
                if parent_category == 3 : _parent_category = _vlst[4]
                ''' делаю эту категрию родительской для остальных'''

                self.t.append({
                'category ID': _vlst[4] ,
                'pail': 1,
                'category name': text,
                'parent category': parent_category,
                'root': 0 ,
                'aliexpress_url' : href
                })

        s.export(data = self.t , format = ['csv'] )
                
    ''' ------------------ КОНЕЦ  -------------------------- '''



    ''' ------------------ НАЧАЛО -------------------------- ''' 
    def build_ALIEXPRESS_categories_table(self , s , start_url : str =''):

        if start_url == '' : start_url = s.supplier_settings_from_json['catalog_wholesale-products']['RU']
        
        s.driver.get_url(start_url)

        main_menu_dict = s.driver.find(s.locators['main_categories_locator_HTMLBLOCK'])
        ''' словарь главных категорий алиэкспресс '''
        blocks_main_items = s.driver.find(s.locators['block_main_items'])
        blocks_sub_items = s.driver.find(s.locators['block_main_items']['block_sub_items'])
        counter = 0 

        #_dict = s.driver.parce_html_block(item , s.locators['block_main_items']['inner level a'])[0]
        categories.fill_categories_table(self , s, main_menu_dict , 3) 
        # 2) подкатегории
        _dict = s.driver.parce_html_block(blocks[counter] , s.locators['block_main_items']['block_sub_items']['inner level a'])[0]
        categories.fill_categories_table(self , s, _dict  , _parent_category) 
        counter +=1


    #''' ------------------ НАЧАЛО -------------------------- '''        
    #def ____build_categories_table(self ,
    #                           locator : dict = None, 
    #                           category_url : str = None , 
    #                           parent_category : int = 3,
    #                           )->bool:

    #        '''parent_category : откуда строится дерево 
    #        s : объект supplier
    #        locator : 
    #        category_url : чаще всего берется из <shop>/all-wholesale-products/
    #        или из parent_category : корень сбора =3 для алиэкспресс в мое каталоге
    #        3 root для алиэкспресс в моем (e-cat.me) дереве категорий
    #        ---------------------
    #        вытаскиваю дерево категорий по локатору
    #        если локатор не задан - начинаю от корня
    #        на самом али и в алишных магазинах могут быть разные локаторы
    #        '''

    #        while tbl_item in self.t:

    #            category_url = tbl_item['category_url']
    #            s.driver.get_url(category_url)

    #            if len(locator.items())==0: locator = s.locators['main_categories_locator_HTMLBLOCK']
    #            ''' нет локатора - беру дефолтный '''
    #            categories.build_sub_categories(self ,s, locator  , tbl_item['category_id'])

            
    #        s.export(data = self.t , format = ['csv'] )
        
    #''' ------------------ КОНЕЦ -------------------------- '''

@attrs
class shop:

    shop_id : int = attrib(init = False , default = None)

    def __attrs_post_init__(self, *args, **kwards):

        pass

    def build_SHOP_categories_table(self):
        pass

@attrs
class products:
    pass



