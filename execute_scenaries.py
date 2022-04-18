import products
from Ini import Ini
import execute_json as jsn
import check_and_convert_datatypes as check_type
from Logging import Log as Log

@Log.logged
def execute_list_of_scenaries(self) ->[] :
    
    ''' по умолчанию все сценарии (имена файлов) прописаны в файе <supplier>.json 
    Каждый сценарий - файл с именем 
    <supplier_name>_categories_<category_name>_<model>_<brand>.json
    при инициализации объекта он хранится в self.scenaries
    
    self - class Supplier (mor, cdata, visual, etc.)


    '''
    for scenario_files in self.scenaries:
        
        for json_file in scenario_files:      
            '''
            загружаю файл сценария из списка <supplier>.json["scenaries"]
            '''
            self.scenaries = jsn.loads( f'''{self.root}\\Ini\\{json_file}''')
            
            #current_p = run_scenario(self)
            run_scenario(self)
           
            '''
            перенесу в run_scenario(self)
            '''
    ''' возвращает список товаров по всему пройденому сценарию'''
    return True

@Log.logged
def run_scenario(self) -> []:
    
    for scenario_node in self.scenaries:
        '''
         -текущий сценарий исполнения состоит из узлов. Каждый узел состоит из:
        - <brand> 
        - [<model>] необязательное поле
        - <url> откуда собирать товары
        - <prestashop_category>
        - <price_rule> пересчет для магазина по умолчанию установливается в self.price_rule
        - <attributes> - свойства товара: цпу, экран, гарантия итп
        '''
        self.current_node = self.scenaries[scenario_node]

        
        build_products_list_by_scenario(self)
        
    '''
    если надо выкидывать каждый сценарий в файл
    '''
    #flush_p(self)



@Log.logged
def build_products_list_by_scenario(self):
    '''
    все товары собираются в 
    список p[]
    каждый элемент списка это словарь с данными о товаре
    '''


    '''
    плохая идея
    '''
    #if self.collect_products_from_categorypage:
    #    sozdaj_spisok_tovarov_zapolini_polia_na_categorypage(self)
    #    # собрал ссылки со страницы категории - 
    #    # возвращаюсь к началу цикла
    #    return True






    '''
    1. собираю ссылки на товары со страниц категории, описанной узлом сценария
    
        ssylki = [] # ссылки на товары 
        
    '''
        #self.log(f''' Собрал ссылки {ssylki}''')
     
    ssylki = soberi_ssylki_na_tovary_by_scenario_node(self)









    ''' Обрабатываю собранные результаты '''


    #а) Не получил страницу  {self.current_nodename["url"]} 
    if ssylki == False or ssylki == None or ssylki == 'None' :
        self.log(f''' !!!!!  Не получил страницу  
        node
        {self.current_node}
        что-то пошло не так при сборе ссылок на страницы товаров 
        ssylki = {ssylki} 
        смотреть в сторону soberi_ssylki_na_tovary_by_scenario_node
        ''')
        return self, False

    #б) Если вернулась строка - запаковавываю ее в список (так бывает, если по сценарию нашелся всего один товар )
    elif str(type(ssylki)).find('str') >-1 : # Строка приходит если нашлась всего одна ссылка
        pass
        ssylki = [ssylki]

    #в) Если пришел список 
    else:
        ssylki = list(set(ssylki)) 
        ''' при помощи set убираю дубликаты '''








    #2 по полученным ссылкам собираю товары
    sozdaj_spisok_tovarov_zapolini_polia(self, ssylki)


@Log.logged
def soberi_ssylki_na_tovary_by_scenario_node(self) ->[]:
    
    try:
        self.log(f'''  получаю ссылки на все товары в категории ''')

        ssylki = []

        ''' нет такой страницы! Возможно, проверить категорию в файле сценария ? '''
        if self.get_url(self.current_node["url"]) == False: 
            self.log(f'''Ошибка перехода по адресу {self.category_url} 
            Возможно, проверить категорию в файле сценария ? 
            {self.current_scenario}''')
            return self, False
   
        #''' на странице категории могут находится  чекбоксы    
        # если их нет, в сценарии JSON они прописаны checkbox = false
        #'''
        json_checkboxes = self.current_node["checkbox"]
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
            scroller(self)


            '''
            _sozdaj_spisok_ssylok_na_stranicy_tovarov_so_stranicy_kategorii
            возвращаает list()
            '''
            ''' собираю ссылки на страницы товаров с текущей страницы категории'''
            ssylki.appened(_sozdaj_spisok_ssylok_na_stranicy_tovarov_so_stranicy_kategorii(self))
            # переключение между страницами
        else:
            while click_to_next_page(self):
                ssylki.appened(_sozdaj_spisok_ssylok_na_stranicy_tovarov_so_stranicy_kategorii(self))
                #self.screenshot(str(s))
                #if check_type.is_none_or_false(ssylki) : 
                #    self.log(f''' ошибка перехода на след страницу категории ''')
                #    continue
                ##ssylki.append()
        return self,ssylki
    except Exception as ex: 
        self.log(f'''Ошибка в функции 
        soberi_ssylki_na_tovary_by_scenario_node(self)
        {ex}''')
        #sys.exit()
      
@Log.logged
def _sozdaj_spisok_ssylok_na_stranicy_tovarov_so_stranicy_kategorii(self ) ->[]:
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
        и вытаскиваю их искомый аттрибуты в виде списка
        '''
        return self.get_listattributes_from_allfound_elements(attribute , link_to_product_locator)
    except: return False


