#######################################################################
#
#   здесь собираются списки товаров от поставщиков
#    
#
#


import pandas as pd
import datetime
import time
import sys
from selenium.common.exceptions import *

from ini_files_dir import Ini
import strings_cleaner as str_cleaner
import price_cleaner
from products import product_fields
import execute_csv as execute_csv
import check_and_convert_datatypes as check_type
from logger import Log

import suppliers.ksp as ksp  # <- WTH??



@Log.log_f
def sozdaj_spisok_tovarov_zapolini_polia(self, urls_tovarov):
    ''' по урл собираю с каждой страницы товара его параметры '''
    try:
        for url in urls_tovarov:
            self.get_url(url)   
            zapolni_paramerty_tovara(self)
    except: return False
















@Log.log_f
def zapolni_paramerty_tovara(self):
    ''' заполняю поля товара '''
    self.p = product_fields.fill_product_fields(self)

    #self.log(f'product_data {product_data}')
    if product == False: #проблема на странице
        self.log(f''' проблема при сборе параметров товара . 
        self.p
        {self.p}
        Пропускаю ''')
        #self.screenshot(f''' проблема при сборе параметров товара . Пропускаю ''')   
        return self, False

@Log.log_f
def insert_product_in_products_list(sel,product):
        try:
            self.products_list.append(product)
            self.log(f''' ############ ТОВАР добавлен     ''')
            return self, True
        except TypeError as ex:
            self.log(f'''АЛЕРТ!  Возникла проблема на сайте 
            {ex} ''')
            #flush_p(self)
            return self, False
        return self




#########################  #########################
#
#
#
#               Нажималки


#################################################


@Log.log_f
def click_to_next_page(self) -> bool:
    '''     Нажималка на след. страницу в  категории    
   Листалка может быть как по страница так по инфинитискролл
   если инфинитискролл, то в локаторе ё пишу
   "selector": "infinity_scroll"
    '''
    if self.locators['category']['pages_listing_locator']['selector'] == 'infinity_scroll':return False

    pager_locator = (self.locators['category']['pages_listing_locator']['by'],
                            self.locators['category']['pages_listing_locator']['selector'])

    element = self.find(pager_locator)

    prev_url = self.driver.current_url

    if element!=False: 
        self.driver.execute_script("window.scrollBy(0,300)") # поднял окошко
        self.log(f''' ---  Тыц на кнопку следующей страницы категории   {element} -----''')
        try:
            if element.click() == False: return False
            if prev_url == self.driver.current_url: return False

            ''' Если не было перехода на след страницу -
            значит сскорее всего она последняя   '''
            return True
        #except ElementNotInteractableException , ElementClickInterceptedException as e:
        except Exception as ex: 
            #self.screenshot(f''' Ошибка перехода на след страницу {ex} ''')
            return False
    else:
        return False
    pass

@Log.log_f
def scroller(self, wait=1 , prokrutok=5, scroll=500):
    '''
    Prokruka stranicy vniz
    '''
    try:
        for i in range(prokrutok):
            self.log(f'------------------------ Скроллинг вниз {i}--------------------------- ')
            self.driver.execute_script(f"window.scrollBy(0,{scroll})") # поднял окошко
            time.sleep(1)
            #self.wait(1)
        return True
    except Exception as ex:
        self.log(str(ex))
        return False

@Log.log_f
def click_checkboxes(self, json_checkboxes):


    #if json_checkboxes == False: return True
    ''' ничего не надо нажимать '''



    #######################################################################################
    #
    #       сценарий ГРАНАДВАНС
    #       
    
    #1
    '''  чекбоксы находятся поd зкрытыми <div>
    открываю их
    '''
    parent_div_selector = ".pr_cn.acc_b"
    by = "css selector"
    parent_div_locator = (by , parent_div_selector)
    parent_divs = self.find(parent_div_locator)
    if parent_divs != False :  # если группа найдена
        for item in parent_divs: 
            if item != False : item.click()


    #2
    ''' нажимаю чекбоксы фильтра товаров '''

    '''
    на сайте постоянно меняется значение чекбоксов. Например,
     "cpu": {
        "class": ".fSel",
        "by": "css selector",
        "value": [
          "CORE I3",
          "CORE I 3",
          "CORE i3",
          "CORE i 3",
          "Core I3",
          "Core I 3",
          "Core i3",
          "Core i 3",
          "I3",
          "I 3",
          "i3",
          "i 3"
        ]

        необходимо перебирать варианты, пока один из них не окажется верным
    '''

    # Чекбоксы ЦПУ

    cpuchecked = chekbox_click_on_group(self , json_checkboxes["cpu"])
    self.log(f''' cpuchecked {cpuchecked} ''')
    screensizechecked = chekbox_click_on_group(self , json_checkboxes["screensize"])
    self.log(f''' screensizechecked {screensizechecked} ''')
    return True

@Log.log_f
def chekbox_click_on_group(self , json_group_checkboxes ):
    checked = False

    for chk in json_group_checkboxes['value']:
        checkbox_selector = str(f'{json_group_checkboxes["class"]}[value="{chk}"]')
        locator = (json_group_checkboxes["by"] , checkbox_selector)
        self.log(f'locator: {locator}')
        checkbox = self.find(locator)
        #self.log(f'checkbox: {checkbox}')
        try:
            if checkbox != False: checkbox.click()
            self.log(f'чекнулся:{checkbox}')
            checked = True
            #return checked

        except AttributeError as ex:
            ''' может найтись несколько одинаковых чекбоксов.
           Может стать проблемой'''
            for item in checkbox: 
                if item != False: item.click()
                self.log(f'чекнулся:{item}')
                checked = True
    
    return checked
@Log.log_f
def check_error_page(self) -> bool:
    self.log( f''' Проверяю страницу на наличие error page ''')
    errors_pages_titles =['Error','עבור לדף המבוקש']
    current_page_title = str(self.driver.title)
    for err__page_title in errors_pages_titles:
        if str(current_page_title).find(err__page_title) >-1:
            self.log(f'''Страница не найдена: 
            {self.driver.current_url} ''')
            return False
    return True


########################################################################




# сбрасываю список товаров полученных от одного сценария
@Log.log_f
def flush_p(self):
    
    if len(self.products_list)==0 : 
        self.log(f''' Пустой список продуктов. Нечего записыавть ''')
        return False

    #self.ps_list = list(set(self.ps_list)) 
    # есть в файле записи csv
    ''' при помощи set убираю дубликаты '''
    dt = Ini.get_now('%d%m%y_%H-%M-%S')
    filename = str(f'{self.supplier}-{dt}.csv')
    path_to_file = str(f'..\\export\\{filename}')
    self.log(f'''   скидываю товары в файл {filename}  ''')
    self.log( f''' Последний успешный сценарий: {self.current_node} ''')
   
    execute_csv.write(self ,  self.products_list , path_to_file)
    self.log(f''' ------------- OK!-------------- ''')
    return True
































def sozdaj_spisok_tovarov_zapolini_polia_na_categorypage(self):
    '''
    Обрабатываю товары напрямую 
    со страницы категории
    Функция :  
    soberi_ssylki_na_tovary_by_scenario_node()
    нужна для правильного отркытия категории

    '''
    
    #try:
    #открываю страницу карегории
    self.get_url(self.current_node["url"])

    #локаторы и селекторы чтобы вытащить блок
    product_block_locator = (self.locators['product']['product_locator']['by'],
                            self.locators['product']['product_locator']['selector'])
    
    attribute = self.locators['product']['product_locator']['attribute']
    self.log(f'''
    <p class="info">Локаторы и селекторы <br>
    link_to_product_locator = 
    {product_block_locator} <br>
    attribute = 
    {attribute}</p>''')
    if self.supplier.find('ksp')>-1:
        scroller(self)
        product_blocks = self.get_listattributes_from_allfound_elements(attribute , product_block_locator)
        # Вытаскиваю из супа поля продуктов
        # и заполняю список
        # self.ps_list
        ksp.pull_products_details_from_blocks(self , product_blocks)
        flush_p(self)
    pass
#except Exception as ex:
    #    self.log(f''' CRASH! {ex} ''')
    #flush_p(self)
    return True