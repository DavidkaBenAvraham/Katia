from typing import List
import execute_json as json
from pathlib import Path
import pandas as pd
from attr import attrib, attrs, Factory

shops : list = []

def login(s):
    locators =  json.loads(Path(s.ini.paths.ini_files_dir , f'''logins.json'''))['aliexpress']
    s.driver.get_url(locators['url'])

    user_locator = (locators['user_locator']['by'], 
                     locators['user_locator']['selector'])
    s.driver.find(locators['user_locator'])[0].send_keys( locators['user'])
    
    password_locator = ( locators['password_locator']['by'],
                         locators['password_locator']['selector'])
    s.driver.find(locators['password_locator'])[0].send_keys( locators['password'])

    send_locator = ( locators['send_locator']['by'],
                         locators['send_locator']['selector'])

    s.driver.find(locators['send_locator'])[0].click()


def get_shops_from_json(s):
    shops_groups_files_dict = json.loads(Path(s.ini.paths.ini_files_dir , f'''aliexpress.json'''))['shops']
    for shop_group_file in shops_groups_files_dict:
        shops_dict = json.loads(Path(s.ini.paths.ini_files_dir , f'''{shop_group_file}'''))
        for item in shops_dict.items() : build_shop_categories(s , item)
    pass 

def build_shop_categories(s , shop_dict : dict) -> dict:
    s.driver.get_url(shop_dict[1]['all-wholesale-products'])
    categoties_group_dict = s.driver.find(s.locators['block_main_items'])[0]

    pass

@attrs
class categories:

    _aliexpress_root_category : int = attrib(init = False , default = 3)
    _category_url : str = attrib(init = False , default = None)
    t : Factory(list) = attrib(init = False , default = None)
    _parent_category : int = attrib(init=False, default = None)  

    def __attrs_post_init__(self, *args, **kwards):
        self._aliexpress_root_category : int = attrib(init = False , default = 3)
        self._category_url = 'https://aliexpress.com/all-wholesale-products.html'
        self.t = []
        self.t.append(
                        {'category ID': 3 ,
                    'pail': 1,
                    'category name': 'ALIEXPRESS',
                    'parent category': 2,
                    'root': 0 ,
                    'category_url' : 'https://aliexpress.com/all-wholesale-products.html'}
                              )
        ''' первая строка таблицы '''

    def fill_categories_table(self , s, html_block : dict = {} ,  parent_category : int = 3) -> bool:
        ''' parent_category : откуда строится дерево 
            3 : root для алиэкспресс в моем (e-cat.me) дереве категорий 
        '''

        
        for k,v in html_block.items():
                _vlst = v.split('/')
                if parent_category == 3 : _parent_category = _vlst[4]
                ''' делаю эту категрию родительской для остальных'''

                self.t.append({
                'category ID': _vlst[4] ,
                'pail': 1,
                'category name': str(k),
                'parent category': parent_category,
                'root': 0 ,
                'aliexpress_url' : v
                })

        s.export(data = self.t , format = ['csv'] )
                
    
    def build_ALIEXPRESS_categories_table(self , s , start_url : str =''):

        if start_url == '' : start_url = s.supplier_settings_from_json['catalog_wholesale-products']['RU']
        
        s.driver.get_url(start_url)

        main_menu_dict = s.driver.find(s.locators['main_categories_locator_HTMLBLOCK'])[0]
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



