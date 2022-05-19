'''
            Функции, присущие поставщику  KSP, которыми я дополняю класс supplier

'''
from logger import Log

from bs4 import BeautifulSoup
import execute_json as json

import sys

import products
from formatter import Formatter

formatter = Formatter() # <- Обязательно переделаю в статический метод

def get_product_fields(self):
    
    '''
    https://stackoverflow.com/questions/34301815/understand-the-find-function-in-beautiful-soup#_=_
    Here we are also checking for presence of data-value attribute.
    soup.find("span", {"class": "real number", "data-value": True})['data-value']
    '''
    p = products.Product()

    p.fields["title"] = formatter.remove_special_characters(self.driver.title)

    '''
    
         Получаю сырые данные со страницы

    '''
  

    

    raw_product_price_supplier = self.find(self.locators['product']['product_price_locator'])

    raw_product_images = ','.join(self.find(self.locators['product']['product_images_locator']))
    raw_product_images_alt = ','.join(self.find(self.locators['product']['product_images_alt_locator']))
    raw_product_sikum = ''.join(self.find(self.locators['product']['product_sikum_locator']))
    combinations = ''.join(self.find(self.locators['product']['product_attributes_locator']))
    raw_product_description = ''.join(self.find(self.locators['product']['product_description_locator']))
    raw_product_mkt_locator = ''.join(self.find(self.locators['product']['product_mkt_locator']))
    




    p.fields["categories"] = self.current_node["prestashop_category"]

    tiur = formatter.remove_special_characters(f'''{raw_product_description}''')

    p.fields["tiur"] = tiur
    p.fields["sikum"] = formatter.remove_special_characters(f'''{raw_product_sikum}''')

    

    p.fields["img url"] = f'''{raw_product_images}'''
    p.fields["img alt"] = f'''{raw_product_images_alt}'''

    p.fields["mkt"] = f'''{raw_product_mkt_locator}'''
    p.fields["mkt suppl"] = f'''{raw_product_mkt_locator}'''
   
   
    price_supplier = formatter.clear_price(f'''{raw_product_price_supplier}''').strip('[]')

    p.fields["mexir lifney"]=price_supplier
    p.fields["mexir olut"]=price_supplier
    p.fields["mexir le yexida"]=price_supplier

    '''
                    Аттрибуты товара


    =================================================================================================


                              "Product ID": "",
                              "Attribute (Name:Type: Position)": "",
                              "value (Name:Type: Position)": "",
                              "Supplier reference": "",
                              "Reference": "",
                              "EAN13": "",
                              "UPC": "",
                              "Wholesale price": "",
                              "Impact on price": "",
                              "Ecotax": "",
                              "Quantity": "",
                              "Minimal quantity": "",
                              "Low stock level": "",
                              "Impact on weight": "",
                              "Default (0/1)": "",
                              "Combination available date": "",
                              "Image position": "",
                              "Image URLs(x,y,z)": "",
                              "Image Alt Text(x,y,z)": "",
                              "shop": "1,2,3,4",
                              "Advanced Stock Mangment": 0,
                              "Depends On Stock": 0,
                              "Warehouse": 0


    



    '''
    product_attributes(self,p,'div',raw_product_description)



    return p.fields

    pass

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




def build_list_from_html_elements(self, delimeter:str, element) -> []:
    '''
    '''
    soup : BeautifulSoup = BeautifulSoup(element , 'html.parser')
    elements_list = soup.findAll(delimeter)
    els :[] = []
    for raw_element in elements_list:
        els.append(formatter.remove_htms_suppliers_and_special_chars(raw_element))
        
    return els



