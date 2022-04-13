'''
Обаработка и заполнение полей товара
'''
import strings_cleaner as str_cleaner
import price_cleaner
import execute_products as product
from Logging import Log as Log
from Ini import Ini
import pandas as pd

def fill_product_fields(self) -> []:
    # return p_fields[]
    # возвращает словарь заполненных полей товара
    # если что-то пойдет не так
    # вернет False
    # знаю, что нельзя менять тип возвращаемого значения

        #Актуально для поставщиков, таких как морлеви
    #''' 
    #Проверка наличия товара 
    #'''
    #if nalihie_segodnja(self) == False :
    #    self.log(f''' -- нет в наличии  {get_sku(self)}--- ''')
    #    return False
    #if product.check_error_page(self) == False: return False
    #supplier_price = get_supplier_price(self)

    #product_name = get_title(self)



    #supplier_price = price_cleaner.convert_to_float_price(self,supplier_price)
    
    #price = eval(self.price_rule) * supplier_price
    #price = price_cleaner.okrugli_krasivo(price)



    ''' таким образом я проверяю доступность страницы
    items_for_control_status_on_page  = [sku , supplier_price, image, product_name]
    #items_for_control_status_on_page  = [price, image, product_name]
    если я не получил один из параметров
    [sku , price, image ,product_name] 
    значит чего-то не хватает
    '''
    #for item in items_for_control_status_on_page:
    #    if item == False or item == -1 or item == None or item=='' :
    #        product.flush_p(self)
    #        self.log(f''' Смотри:
    #       sku = {sku}, 
    #       price = {price}, 
    #       image = {image}, 
    #       product_name = {product_name}
    #       url: {self.driver.current_url}''')
    #        return False
    
    self.p = dict(self.fields)
    
    try:
        self.p['Title'] = get_title(self)
        self.p['category'] = str(f'{str(self.current_node["prestashop_category"])}')
        self.p['Supplier Reference'] = self.p['Title']
        self.p['Reference'] =  self.p['Title']
        #self.p['manufacrurer reference'] = get_brand_sku(self)
        #self.p['manufacrurer reference'] = ''

        self.p['Available for Order'] = '1'
        self.p['Condition'] = 'new'
        self.p['show_price'] = '1'
        
        self.p['Tax rules ID'] = '53'
        #self.p['Supplier'] = self.supplier_name
        self.p['Supplier'] = ''
        self.p['Visibility'] = 'both'


        self.p['Price'] = get_price(self)
        #self.log( f''' цена на сайте {self.p['Price']}''')
        #self.p['Supplier Price (Tax Excl.)'] = str(supplier_price)
        #self.log( f''' цена поставщика до маам {self.p['Supplier Price (Tax Excl.)']}''')

        self.p['brand'] = self.current_node["brand"]
        #self.p['Short Description'] = self.p['Product Name']
        #self.p['Short Description'] = get_short_description(self)
        #self.p['Short Description'] = str_cleaner.cut_field_to_size(self, self.p['Short Description'], 1800)
        self.p['Short Description'] = str_cleaner.cut_field_to_size(self, get_short_description(self), 1800)
        self.p['Description'] = self.p['Short Description']
        #self.p['Description'] = str_cleaner.remove_unnecessary_words(self,str(get_description(self)))
        #self.p['Description'] = str_cleaner.cut_field_to_size(self, self.p['Description'], 9000)
        
        #self.p['Description'] = str_cleaner.cut_field_to_size(self, str(get_description(self), 9000))
        self.p['Product Images'] = get_images(self)
        self.p['Product Image Alt.'] = f'''{self.p['brand']} {self.p['Title']}'''


        #self.log(f''' self.p['Supplier Reference'] = {self.p['Supplier Reference']}  ''')

        self.p['meta descrition'] =  self.p['Title']

    
    
        self.p['delete old images'] = '1'
        self.p['meta_words'] = str(get_meta(self,p_fields))
        self.p['Active'] = 1
        #self.p['RAW_PAGE_SOURCE'] = self.driver.page_source
        self.p['QTY'] = '10'


        #check_for_videochipset(p_fields)

        #p_fields = obrabotaj_polja_tovara(p_fields)
        '''поля товара обрабатываются в зависимости от сайта 
        функция обработки находится в product.py каждого из поставщиков 
        и вызывается через __init__.obrabotaj_polja_tovara(p_fields)
        '''
        #self.log( f''' Поля товара {p_fields}''')
        return p_fields
    except Exception as e:
        self.log( f''' Ошибка при напонении полей словаря товаров {e}''')
        self.log( f''' Поля товара {p_fields}''')
        return False




def get_title(self) -> str:
    
    title_locator = (
                     self.locators['product_fields_locators']['title_locator']['by'],
                    self.locators['product_fields_locators']['title_locator']['selector'])
  
    attribute = self.locators['product_fields_locators']['title_locator']['attribute']
    title = self.get_attribute_from_first_found_element(attribute , title_locator)

    title = str_cleaner.remove_unnecessary_words(self, title)

    if title == False : return False # серьезный сбой
    str_cleaner.cut_field_to_size(self, title , 120)
    return title.upper()

def get_brand_from_title(self, p_fields: []) -> str:
    if p_fields.__contains__('Product Name'): 
        p_fields["Product Name"] = str(p_fields["Product Name"]).upper()
        for brand in self.brands:
            b = str(brand).upper()
            if str(p_fields["Product Name"]).find(b) >-1: 
                return str_cleaner.clean_string(self , brand)
    pass
def get_brand_from_webpage(self, p_fields: []) -> str:
    brand_locator  = (
        self.locators['product_fields_locators']['brand_locator']['by'],
        self.locators['product_fields_locators']['brand_locator']['selector'])
    attribute = self.locators['product_fields_locators']['brand_locator']['attribute']
    return self.get_attribute_from_first_found_element(attribute, brand_locator)
    
def remove_brand_from_title(self, p_fields: []):
    if p_fields.__contains__('Product Name'): 
        p_fields["Product Name"] = str(p_fields["Product Name"]).upper()
        for brand in self.brands:
            brand = str(brand).upper()
            if str(p_fields["Product Name"]).find(brand) >-1: 
                p_fields["Product Name"] = str(p_fields["Product Name"]).replace(brand , '')
    pass
def get_brand_sku(self) -> str:
    brand_sku_locator = (
                         self.locators['product_fields_locators']['brand_sku_locator']['by'],
                                self.locators['product_fields_locators']['brand_sku_locator']['selector'])
    attribute = self.locators['product_fields_locators']['brand_sku_locator']['attribute']
    return self.get_attribute_from_first_found_element(attribute, brand_sku_locator)
 
def get_price(self) :
    price_locator = (
                     self.locators['product_fields_locators']['price_locator']['by'],
                                  self.locators['product_fields_locators']['price_locator']['selector'])
    attribute = self.locators['product_fields_locators']['price_locator']['attribute']
    
    price = self.get_attribute_from_first_found_element(attribute, price_locator)
    if price == None: return -1
    #self.log (f''' найдена цена {price} ''')
    return price_cleaner.convert_to_float_price(self ,price)
    
def get_supplier_price(self) -> str:
   
    price_locator = (
                     self.locators['product_fields_locators']['price_locator']['by'],
                                  self.locators['product_fields_locators']['price_locator']['selector'])
    attribute = self.locators['product_fields_locators']['price_locator']['attribute']
    
    price = self.get_attribute_from_first_found_element(attribute, price_locator)
    if price == None: return ''
    self.log.write(self,f''' найдена цена {price} ''')
    return price

def get_sku(self):

    sku_locator = (
        self.locators['product_fields_locators']['sku_locator']['by'],
                        self.locators['product_fields_locators']['sku_locator']['selector'])
    attribute = self.locators['product_fields_locators']['sku_locator']['attribute']
    sku = self.get_attribute_from_first_found_element(attribute, sku_locator)
    if sku == None: return ''
    sku = str_cleaner.clean_string(self, sku)
    #self.log(f'''     --- sku {sku} ---    ''')
    return sku

def get_short_description(self , alert = ''):

    short_description_locator = (
                                 self.locators['product_fields_locators']['short_description_locator']['by'],
                            self.locators['product_fields_locators']['short_description_locator']['selector'])
    attribute = self.locators['product_fields_locators']['short_description_locator']['attribute']
    ''' здесь можно оставить алерт или сообщение для клиента'''
    element = self.get_attribute_from_first_found_element(attribute, short_description_locator)
    if element == False: element = ''

    return element


def get_description(self , alert = ''):
    # добавляю дату обновления
    #dt = Ini.get_now('%d/%m')
    #dt = str(f'''<p font-size="x-small" color="" >upd: {dt}</p>''')

    description_locator = (
                           self.locators['product_fields_locators']['description_locator']['by'],
                                self.locators['product_fields_locators']['description_locator']['selector'])
    attribute = self.locators['product_fields_locators']['description_locator']['attribute']

    ''' здесь можно оставить алерт '''
    element = self.get_attribute_from_first_found_element(attribute, description_locator)
    if element == False: element = ''

    return str(f''' {element} ''')

def get_images(self) -> []:
    image_locator = (
                     self.locators['product_fields_locators']['image_locator']['by'],
                             self.locators['product_fields_locators']['image_locator']['selector'])
    attribute = self.locators['product_fields_locators']['image_locator']['attribute']
    
    images_list = self.get_listattributes_from_allfound_elements(attribute, image_locator)
    images_list = list(set(images_list))
    images_str = str(list(set(images_list)))
    images_str = str(images_str).replace("[", "")
    images_str = str(images_str).replace("]", "")
    images_str = str(images_str).replace("'", "")
    return images_str

def get_meta(self,p_fields):
    meta_words = ''
    if p_fields.__contains__('brand'):
        meta_words += self.p['brand'] + ' '
    if p_fields.__contains__('Title'):
        meta_words += str( self.p['Title']) + ' '
    #if p.__contains__('Product Name'):
    #    meta_words += self.p['Product Name'] + ' '
   
    return meta_words

def nalihie_segodnja(self) -> bool:
    '''
    на странице товара проверяю по локатору stock_locator ключевые слова,
    указывающие на отсутствие товара у поставщика
    '''
    stock_locator = (
                     self.locators['stock_locator']['by'],
                            self.locators['stock_locator']['selector'])
    attribute = self.locators['stock_locator']['attribute']
    element = self.get_attribute_from_first_found_element(attribute, stock_locator)
   
    if element == False : return True #нет элемента - значит есть в наличии ?
    if str(type(element)).find('NoneType') >-1: return True #нет такого элемента ?
    stock_alert = ["חסר במלאי",
                   "מלאי בדרך",
                   "מלאי חסר" , 
                   "זמינות מוגב" , 
                   "חסר",
                   "מוגב",
                   "אזל מהמלאי",
                   "בדרך"]
    for alert in stock_alert: 
        if element.find(alert)>-1: return False # нет в наличии
    return True


def check_for_videochipset(p_fields:[]) -> None:
    """ вытаскиваю модели видеочипов из названия товара """

    product_title = self.p['Product Name']
    if str(self.p['category']).find('108')<0: return True
    ''' если не категория видео - ухожу '''

    if str(product_title).find('210')>0  :self.p['category'] += ',583'
    if str(product_title).find('710')>0  :self.p['category'] += ',584'
    if str(product_title).find('730')>0  :self.p['category'] += ',585'
    if str(product_title).find('1030')>0  :self.p['category'] += ',586'
    if str(product_title).find('1050')>0  :
        if str(product_title).find('TI')>0:self.p['category'] += ',588'
        else:self.p['category'] += ',587'

    if str(product_title).find('1080')>0  :
        if str(product_title).find('TI')>0:self.p['category'] += ',590'
        else:self.p['category'] += ',589'

    if str(product_title).find('1650')>0  :
        if str(product_title).find('TI')>0:self.p['category'] += ',592'
        elif str(product_title).find('SUPER')>0 or str(product_title).find('1650S')>0 :self.p['category'] += ',593'
        else:self.p['category'] += ',501'

    if str(product_title).find('1660')>0  :
        if str(product_title).find('SUPER')>0 or str(product_title).find('1660S')>0 :self.p['category'] += ',595'
        else:self.p['category'] += ',594'

    if str(product_title).find('2060')>0  :
        if str(product_title).find('SUPER')>0 or str(product_title).find('2060S')>0 :self.p['category'] += ',597'
        else:self.p['category'] += ',596'

    if str(product_title).find('2070')>0  :
        if str(product_title).find('SUPER')>0 or str(product_title).find('2060S')>0 :self.p['category'] += ',599'
        else:self.p['category'] += ',598'

    if str(product_title).find('2080')>0  :
        if str(product_title).find('TI')>0:self.p['category'] += ',601'
        elif str(product_title).find('SUPER')>0 or str(product_title).find('1650S')>0 :self.p['category'] += ',602'
        else:self.p['category'] += ',600'

    if str(product_title).find('3070')>0 :self.p['category'] += ',603'
    if str(product_title).find('3080')>0 :self.p['category'] += ',604'
    if str(product_title).find('3090')>0 :self.p['category'] += ',605'

def obrabotaj_polja_tovara(p_fields):
    ''' здесь находится логика постобработки '''
    if str(self.p['Product Name']).find("#") >-1 : self.p['Product Name'] = str(self.p['Product Name'])[0:-12]
    self.p['Product Name'] = str(self.p['Product Name']).replace("#", '')
    self.p['RAW_PAGE_SOURCE'] = ''

    return p_fields