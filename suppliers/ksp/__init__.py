'''
            Функции, присущие поставщику  KSP, которыми я дополняю класс supplier

'''
from logger import Log

from bs4 import BeautifulSoup
import execute_json as json
from strings_formatter import StringFormatter
formatter = StringFormatter(
from suppliers.product import Product 
def product_attributes(self, p, delimeter, elements):
    i=0
    skip = False
    c = p.combinations 
    ''' просто сокращенная запись '''
    for e in build_list_from_html_elements(self, delimeter, elements):
        if i%2 == 0:

            if not p.skip_row(e):
                '''
                -----^^^^^^^^^^   
                слова в колонке, которые надо пропустить находятся в файле
                prestashop_product_combinations_sysnonyms_<lg>.json['skip']
                '''
                i+=1
                skip = True
                continue

            attr = formatter.remove_HTML_tags(e)
            ''' первое значение '''
            if c["Attribute (Name:Type: Position)"] == "": c["Attribute (Name:Type: Position)"] = f'''{attr}:select:0'''
            else: c["Attribute (Name:Type: Position)"] += f''', {attr}:select:0'''
            ''' остальные значения '''
        else:
            if skip:
                i+=1        
                skip = False
                continue

            val = e.next
            if c["value (Name:Type: Position)"] == "":c["value (Name:Type: Position)"] = f'''{e.next}:select:0'''
            else: c["value (Name:Type: Position)"] += f''',{e.next}:select:0'''
        i+=1
        pass


def grab_product_page(s):
    _d = s.driver
    _d.scroll(3)
    _ : dict = s.locators['product']

    p : Product = Product(s=s).grab_product_page()
    field = p.fields

    def get_id():
        field['id'] = _d.find(_['product_mkt_locator'])
       
    def get_title():
        field['title'] = _d.find(_['product_title_locator'])
    def get_price():
        _price = _d.find(_['product_price_locator'])
        field['price'] = formatter.clear_price(_price)
    def get_shipping():
        _shipping = _d.find(_['product_shipping_locator'])
        for s in _shipping:
            field['shipping price'] = formatter.clear_price(s)
    def get_images():
        _images = _d.find(_['product_images_locator'])
        for k,v in _images.items():
               field['img url'] += f''' {v}, '''
               field['img alt'] += f''' {k}, '''
    def get_attributes():
        _attributes = _d.find(_['product_attributes_locator'])
        return _attributes
    def get_qty():
        _qty = _d.find(_['product_qty_locator'])
        _qty = formatter.clear_price(_qty)
        return _qty
    def get_byer_protection():
        _byer_protection = _d.find(_['product_byer_protection_locator'])
        return _byer_protection
    def get_description():
        _description = _d.find(_['product_description_locator'])
        return _description
    def get_specification():
        specification = _d.find(_['product_specification_locator'])
        return specification
    def get_customer_reviews():
        _customer_reviews = _d.find(_['product_customer_reviews_locator'])
        return _customer_reviews



    get_id(),
    get_title(),
    get_price(),
    get_shipping(),
    get_images(),
    get_attributes(),
    get_qty(),
    get_byer_protection(),
    get_description(),
    get_specification(),
    get_customer_reviews()
        

    pass



