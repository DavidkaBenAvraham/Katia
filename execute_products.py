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

from Ini import Ini
import strings_cleaner as str_cleaner
import price_cleaner
import product_fields
import execute_csv as execute_csv
import check_and_convert_datatypes as check_type
from Logging import Log as Log
import suppliers.ksp as ksp

@Log.log_f
def build_produscts_list_by_scenario(self):
    '''
    все товары собираются в 
    список p[]
    каждый элемент списка это словарь с данными о товаре
    '''
 

    for scenario_node in self.json_scenario:
        '''
         -текущий сценарий исполнения состоит из узлов. Каждый узел состоит из:
        - <brand> 
        - [<model>] необязательное поле
        - <url> откуда собирать товары
        - <prestashop_category>

        

'''     '''
        self.currentscenario_nodename - название текущего узла сценария
        self.currentscenario_node - весь узел 
        Таки важны оба. 
        '''
        #self.currentscenario_nodename = scenario_node
        self.currentscenario_node = self.json_scenario[scenario_node]
        '''
        Добавлена возможность собирать товары со страницы
        категории. Пример - ksp        
        Устанавливается в файле ksp.json
        "collect_products_from_categorypage": true,
        '''
        if self.collect_products_from_categorypage:
            sozdaj_spisok_tovarov_zapolini_polia_na_categorypage(self)
            # собрал ссылки со страницы категории - 
            # возвращаюсь к началу цикла
            continue

        #1 собираю ссылки на товары со страниц категории, описанной узлом сценария
        #p_hrefs = [] # ссылки на товары 
        p_hrefs = sozdaj_ssylki_na_tovary_by_scenario_node(self)
        #self.log(f''' Собрал ссылки {p_hrefs}''')
        
        ''' Обработка собранных результатов '''

        #а) Не получил страницу  {self.currentscenario_nodename["url"]} 
        if p_hrefs == False or p_hrefs == None or p_hrefs == 'None' :
            self.log(f''' !!!!!  что-то пошло не так при сборе ссылок на страницы товаров p_hrefs = {p_hrefs} 
            смотреть в сторону sozdaj_ssylki_na_tovary_by_scenario_node
            ''')
            continue
        #б) Если вернулась строка - запаковавываю ее в список (так бывает, если по сценарию нашелся всего один товар )
        elif str(type(p_hrefs)).find('str') >-1 : # Строка приходит если нашлась всего одна ссылка
            pass
            p_hrefs = [p_hrefs]
        #в) Если пришел список 
        else:
            p_hrefs = list(set(p_hrefs)) 
            ''' при помощи set убираю дубликаты '''

        #2 по полученным ссылкам собираю товары
        sozdaj_spisok_tovarov_zapolini_polia(self, p_hrefs)

        #flush_p(self)
    return self.products_list

@Log.log_f
def sozdaj_ssylki_na_tovary_by_scenario_node(self):
    
    try:
        self.log(f'''  получаю ссылки на все товары в категории ''')

        ssylki = []

        ''' нет такой страницы! Возможно, проверить категорию в файле сценария ? '''
        if self.get_url(self.currentscenario_node["url"]) == False: 
            self.log(f'''Ошибка перехода по адресу {self.category_url} 
            Возможно, проверить категорию в файле сценария ? ''')
            return False
   
        #''' на странице категории могут находится  чекбоксы    
        # если их нет, в сценарии JSON они прописаны checkbox = false
        #'''
        json_checkboxes = self.currentscenario_node["checkbox"]
        if json_checkboxes: 
            click_checkboxes(self, json_checkboxes) 
            self.log(f''' есть чекбоксы {json_checkboxes}''')
        ################ if check_error_page(self) == False: return False
    


        # Если на сайте для показа товаров я использую прокрутку вниз
        if self.locators['infinity_scroll'] == True: 
            ''' на сайте вижуал есть бесконечная прокутка 
            сдвиг по бесконечной прокрутке включается флагом 
            json_infinity_scroll в файле сценария поставщика
            '''
            try: scroller(self)
            except Exception as ex: self.log(f'''
          ошибка при прокрутке
          {ex}
            ''')


            '''
            sozdaj_spisok_ssylok_na_stranicy_tovarov_so_stranicy_kategorii
            возвращаает list()
            '''
            ''' собираю ссылки на страни
            цы товаров с текущей страницы категории'''
            ssylki.appened(sozdaj_spisok_ssylok_na_stranicy_tovarov_so_stranicy_kategorii(self))
            # переключение между страницами
        else:
            while click_to_next_page(self):
                ssylki.appened(sozdaj_spisok_ssylok_na_stranicy_tovarov_so_stranicy_kategorii(self))
                #self.screenshot(str(s))
                #if check_type.is_none_or_false(ssylki) : 
                #    self.log(f''' ошибка перехода на след страницу категории ''')
                #    continue
                ##ssylki.append()
        return ssylki
    except Exception as ex: 
        self.log(f'''{ex}''')
        sys.exit()
      
@Log.log_f
def sozdaj_spisok_ssylok_na_stranicy_tovarov_so_stranicy_kategorii(self ):
    try:
        ''' когда я нахожусь на странице категории я собираю ссылки на товары со страницы.
        Страниц может быть несколько, в таком случае я пользуюсь листалкой, чтобы собраь все
        ссылки на вс товары со всех страниц
        '''


        self.log(f''' Создаю список ссылок на стрницы товаров ''')
        link_to_product_locator = (self.locators['product']['product_locator']['by'],
                                self.locators['product']['product_locator']['selector'])
    
        attribute = self.locators['product']['product_locator']['attribute']
        log_str = str(f'''
        <p class="info">Локаторы и селекторы <br>
        link_to_product_locator = 
        {link_to_product_locator} <br>
        attribute = 
        {attribute}</p>''')
        #self.log(log_str)
        '''
        Нашел на странице категории по локаторам 
        элементы ведущие на страницу товаров
        и вытаскиваю их искомый аттрибут
        '''
        return self.get_listattributes_from_allfound_elements(attribute , link_to_product_locator)
    except: return False
@Log.log_f
def sozdaj_spisok_tovarov_zapolini_polia(self, urls_tovarov):
    ''' по урл собираю с каждой страницы товара его параметры '''
    try:
        for url in urls_tovarov:
            self.get_url(url)   
            zapolni_paramerty_tovara(self)
    except: return False


def sozdaj_spisok_tovarov_zapolini_polia_na_categorypage(self):
    '''
    Обрабатываю товары напрямую 
    со страницы категории
    Функция :  
    sozdaj_ssylki_na_tovary_by_scenario_node()
    нужна для правильного отркытия категории

    '''
    
    #try:
    #открываю страницу карегории
    self.get_url(self.currentscenario_node["url"])

    #лоцаторы и селекторы чтобы вытащить блок
    product_block_locator = (self.locators['product']['product_locator']['by'],
                            self.locators['product']['product_locator']['selector'])
    
    attribute = self.locators['product']['product_locator']['attribute']
    self.log(f'''
    <p class="info">Локаторы и селекторы <br>
    link_to_product_locator = 
    {product_block_locator} <br>
    attribute = 
    {attribute}</p>''')
    if self.supplier_name.find('ksp')>-1:
        try:
            scroller(self)
        except: pass
        product_blocks = self.get_listattributes_from_allfound_elements(attribute , product_block_locator)
        # Вытаскиваю из супа поля продуктов
        # и заполняю список
        # self.products_list
        ksp.pull_products_details_from_blocks(self , product_blocks)
        flush_p(self)
    pass
#except Exception as ex:
    #    self.log(f''' CRASH! {ex} ''')
    #flush_p(self)
    return True

@Log.log_f
def zapolni_paramerty_tovara(self):
    ''' заполняю поля товара '''
    product_data = product_fields.fill_product_fields(self)
    #self.log(f'product_data {product_data}')
    if product_data == False: #проблема на странице
        #self.screenshot(f''' проблема при сборе параметров товара . Пропускаю ''')   
        return False
    else: 
        try:
            self.products_list.append(product_data)
            self.log(f''' ############ ТОВАР добавлен     ''')
            return True
        except TypeError as ex:
            self.log(f'''АЛЕРТ!  Возникла проблема на сайте 
            {ex} ''')
            #flush_p(self)
            return False
    return self.products_list




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

def scroller(self, wait=1 , prokrutok=3, scroll=800):
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
        return False,ex

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

    #self.products_list = list(set(self.products_list)) 
    # есть в файле записи csv
    ''' при помощи set убираю дубликаты '''
    dt = Ini.get_now('%d%m%y_%H-%M-%S')
    filename = str(f'{self.supplier_prefics}-{dt}.csv')
    path_to_file = str(f'..\\export\\{filename}')
    self.log(f'''   скидываю товары в файл {filename}  ''')
    self.log( f''' Последний успешный сценарий: {self.currentscenario_node} ''')
   
    execute_csv.write(self ,  self.products_list , path_to_file)
    self.log(f''' ------------- OK!-------------- ''')
    return True