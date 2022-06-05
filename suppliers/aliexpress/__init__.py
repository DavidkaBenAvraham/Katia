from typing import List
import execute_json as json
from pathlib import Path
import pandas as pd
from attr import attrib, attrs, Factory


@attrs
class categories:

    _aliexpress_root_category : int = attrib(init = False , default = 3)
    _category_url : str = attrib(init = False , default = None)
    t : Factory(list) = attrib(init = False , default = None)
    _parent_category : int = attrib(init=False, default = None)  

    def __attrs_post_init__(self, *args, **kwards):
        self._aliexpress_root_category : int = attrib(init = False , default = 3)
        self._category_url = 'https://aliexpress.ru/all-wholesale-products.html'
        self.t = []
        self.t.append(
                        {'category ID': 3 ,
                    'pail': 1,
                    'category name': 'ALIEXPRESS',
                    'parent category': 2,
                    'root': 0 ,
                    'category_url' : 'https://aliexpress.ru/all-wholesale-products.html'}
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

    ''' ------------------ НАЧАЛО -------------------------- '''        
    def ____build_categories_table(self ,
                               locator : dict = None, 
                               category_url : str = None , 
                               parent_category : int = 3,
                               )->bool:

            '''parent_category : откуда строится дерево 
            s : объект supplier
            locator : 
            category_url : чаще всего берется из <shop>/all-wholesale-products/
            или из parent_category : корень сбора =3 для алиэкспресс в мое каталоге
            3 root для алиэкспресс в моем (e-cat.me) дереве категорий
            ---------------------
            вытаскиваю дерево категорий по локатору
            если локатор не задан - начинаю от корня
            на самом али и в алишных магазинах могут быть разные локаторы
            '''

            while tbl_item in self.t:

                category_url = tbl_item['category_url']
                s.driver.get_url(category_url)

                if len(locator.items())==0: locator = s.locators['main_categories_locator_HTMLBLOCK']
                ''' нет локатора - беру дефолтный '''
                categories.build_sub_categories(self ,s, locator  , tbl_item['category_id'])

            
            s.export(data = self.t , format = ['csv'] )
        
    ''' ------------------ КОНЕЦ -------------------------- '''

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


def build_shops_list_from_scenaries_files(s , scenaries_files : list = []) -> dict:

    print(scenaries)
