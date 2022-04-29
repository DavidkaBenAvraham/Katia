'''
Обаработка и заполнение полей товара
'''
import strings_cleaner as str_cleaner
import price_cleaner
import products 
#import products.execute_products as product
from logger import Log
from ini_files import Ini
from suppliers import Supplier



def generate_product(self:Supplier) -> bool:

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
    
    p = Product()

    #self.p = dict(self.fields)
    
    try:
        p.fields['Title'] = get_title(self)
        p.fields['category'] = str(f'{str(self.current_node["prestashop_category"])}')
        p.fields['Supplier Reference'] = p.fields['Title']
        p.fields['Reference'] =  p.fields['Title']
        #p.fields['manufacrurer reference'] = get_brand_sku(self)
        #p.fields['manufacrurer reference'] = ''

        p.fields['Available for Order'] = '1'
        p.fields['Condition'] = 'new'
        p.fields['show_price'] = '1'
        
        p.fields['Tax rules ID'] = '53'
        #p.fields['Supplier'] = self.supplier_name
        p.fields['Supplier'] = ''
        p.fields['Visibility'] = 'both'


        p.fields['Price'] = get_price(self)
        #self.log( f''' цена на сайте {p.fields['Price']}''')
        #p.fields['Supplier Price (Tax Excl.)'] = str(supplier_price)
        #self.log( f''' цена поставщика до маам {p.fields['Supplier Price (Tax Excl.)']}''')

        p.fields['brand'] = self.current_node["brand"]
        #p.fields['Short Description'] = p.fields['Product Name']
        #p.fields['Short Description'] = get_short_description(self)
        #p.fields['Short Description'] = str_cleaner.cut_field_to_size(self, p.fields['Short Description'], 1800)
        p.fields['Short Description'] = str_cleaner.cut_field_to_size(self, get_short_description(self), 1800)
        p.fields['Description'] = p.fields['Short Description']
        #p.fields['Description'] = str_cleaner.remove_unnecessary_words(self,str(get_description(self)))
        #p.fields['Description'] = str_cleaner.cut_field_to_size(self, p.fields['Description'], 9000)
        
        #p.fields['Description'] = str_cleaner.cut_field_to_size(self, str(get_description(self), 9000))
        p.fields['Product Images'] = get_images(self)
        p.fields['Product Image Alt.'] = f'''{p.fields['brand']} {p.fields['Title']}'''


        #self.log(f''' p.fields['Supplier Reference'] = {p.fields['Supplier Reference']}  ''')

        p.fields['meta descrition'] =  p.fields['Title']

    
    
        p.fields['delete old images'] = '1'
        p.fields['meta_words'] = str(get_meta(self,p_fields))
        p.fields['Active'] = 1
        #p.fields['RAW_PAGE_SOURCE'] = self.driver.page_source
        p.fields['QTY'] = '10'


        #check_for_videochipset(p_fields)

        #p_fields = obrabotaj_polja_tovara(p_fields)
        '''поля товара обрабатываются в зависимости от сайта 
        функция обработки находится в product.py каждого из поставщиков 
        и вызывается через __init__.obrabotaj_polja_tovara(p_fields)
        '''
        #self.log( f''' Поля товара {p_fields}''')
        self.p.append(p)
        return self, True
    except Exception as e:
        self.log( f''' Ошибка при напонении полей словаря товаров {e}''')
        self.log( f''' Поля товара {p_fields}''')
        return self, False




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
        meta_words += p.fields['brand'] + ' '
    if p_fields.__contains__('Title'):
        meta_words += str( p.fields['Title']) + ' '
    #if p.__contains__('Product Name'):
    #    meta_words += p.fields['Product Name'] + ' '
   
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

    product_title = p.fields['Product Name']
    if str(p.fields['category']).find('108')<0: return True
    ''' если не категория видео - ухожу '''

    if str(product_title).find('210')>0  :p.fields['category'] += ',583'
    if str(product_title).find('710')>0  :p.fields['category'] += ',584'
    if str(product_title).find('730')>0  :p.fields['category'] += ',585'
    if str(product_title).find('1030')>0  :p.fields['category'] += ',586'
    if str(product_title).find('1050')>0  :
        if str(product_title).find('TI')>0:p.fields['category'] += ',588'
        else:p.fields['category'] += ',587'

    if str(product_title).find('1080')>0  :
        if str(product_title).find('TI')>0:p.fields['category'] += ',590'
        else:p.fields['category'] += ',589'

    if str(product_title).find('1650')>0  :
        if str(product_title).find('TI')>0:p.fields['category'] += ',592'
        elif str(product_title).find('SUPER')>0 or str(product_title).find('1650S')>0 :p.fields['category'] += ',593'
        else:p.fields['category'] += ',501'

    if str(product_title).find('1660')>0  :
        if str(product_title).find('SUPER')>0 or str(product_title).find('1660S')>0 :p.fields['category'] += ',595'
        else:p.fields['category'] += ',594'

    if str(product_title).find('2060')>0  :
        if str(product_title).find('SUPER')>0 or str(product_title).find('2060S')>0 :p.fields['category'] += ',597'
        else:p.fields['category'] += ',596'

    if str(product_title).find('2070')>0  :
        if str(product_title).find('SUPER')>0 or str(product_title).find('2060S')>0 :p.fields['category'] += ',599'
        else:p.fields['category'] += ',598'

    if str(product_title).find('2080')>0  :
        if str(product_title).find('TI')>0:p.fields['category'] += ',601'
        elif str(product_title).find('SUPER')>0 or str(product_title).find('1650S')>0 :p.fields['category'] += ',602'
        else:p.fields['category'] += ',600'

    if str(product_title).find('3070')>0 :p.fields['category'] += ',603'
    if str(product_title).find('3080')>0 :p.fields['category'] += ',604'
    if str(product_title).find('3090')>0 :p.fields['category'] += ',605'

def obrabotaj_polja_tovara(p_fields):
    ''' здесь находится логика постобработки '''
    if str(p.fields['Product Name']).find("#") >-1 : p.fields['Product Name'] = str(p.fields['Product Name'])[0:-12]
    p.fields['Product Name'] = str(p.fields['Product Name']).replace("#", '')
    p.fields['RAW_PAGE_SOURCE'] = ''

    return p_fields