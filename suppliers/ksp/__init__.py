from logger import Log
# примеры 
# https://python-scripts.com/beautifulsoup-html-parsing
from bs4 import BeautifulSoup
import price_cleaner
import re
import json
import execute_json as jsn
import _regex as rgf
import sys
import price_cleaner
import strings_cleaner
import products
from string_formatter import Formatter


'''



                      "id": "",
                      "pail": 1,
                      "title": "",
                      "categories": "",
                      "mexir lifney": "",
                      "mezhe mas": 53,
                      "mexir olut": "",
                      "onsale": "1",
                      "gova or kamut anaha": "",
                      "anaxa axuzim": "",
                      "anaxa mtaarix  (yyyy-mm-dd)": "",
                      "anaxa ad taarix (yyyy-mm-dd)": "",
                      "mkt": "",
                      "mkt suppl": "",
                      "supplier": "",
                      "brand": "",
                      "EAN-13": "",
                      "UPC": "",
                      "MPN": "",
                      "green тах": "",
                      "roxav": "",
                      "gova": "",
                      "omek": "",
                      "mishkal": "",
                      "zman aspaka": "",
                      "Delivery time of out-of-stock products": "",
                      "qty": "10",
                      "min qty": "1",
                      "ramat mlay nemuha": "",
                      "doar mlay": "",
                      "visible": "both",
                      "alut mishloh": "50",
                      "yehida avur mexir yaxida": "",
                      "mexir le yexida": "",
                      "sikum": "",
                      "tiur": "",
                      "tagiot": "",
                      "koteret meta": "",
                      "milot mafeah": "",
                      "tiur meta": "",
                      "rewrie url": "",
                      "tavit im bemlay": "",
                      "back-order": "",
                      "zamin-azmana": "1",
                      "taarix zminut": "",
                      "shnat yatzur": "",
                      "price visible": "1",
                      "img url": "",
                      "img alt": "",
                      "mexika tmuna kodemet": "1",
                      "maafianim mufradim bpsik": "",
                      "zamin rak breshet": "0",
                      "matzav": "",
                      "nitan leatama": "",
                      "kvatzim": "",
                      "sadot text": "1",
                      "peula im azal": "",
                      "virtuali": "",
                      "url file": "",
                      "mispar hudaot": "",
                      "taarix tfuga": "",
                      "mispar yamim": "",
                      "id xanut": "1,2,3,4",
                      "nihul mlai mitkadem": 0,
                      "taluj bmalay": 0,
                      "maxsan": "",
                      "avizarim": ""



'''






def build_product(self):
    
    '''
    https://stackoverflow.com/questions/34301815/understand-the-find-function-in-beautiful-soup#_=_
    Here we are also checking for presence of data-value attribute.
    soup.find("span", {"class": "real number", "data-value": True})['data-value']
    '''
    p = products.Product(self.lang)
    p.fields["Title"] = self.driver.title

    '''
    
         Получаю сырые данные со страницы

    '''
  
    raw_product_price_supplier = ''.join(self.get_elements_by_locator(self.locators['product']['product_price_locator']))
    raw_product_images = ','.join(self.get_elements_by_locator(self.locators['product']['product_images_locator']))
    raw_product_images_alt = ','.join(self.get_elements_by_locator(self.locators['product']['product_images_alt_locator']))
    raw_product_sikum = ''.join(self.get_elements_by_locator(self.locators['product']['product_sikum_locator']))
    combinations = ''.join(self.get_elements_by_locator(self.locators['product']['product_attributes_locator']))
    raw_product_description = ''.join(self.get_elements_by_locator(self.locators['product']['product_description_locator']))
    raw_product_mkt_locator = ''.join(self.get_elements_by_locator(self.locators['product']['product_mkt_locator']))
    

    p.fields["categories"] = self.current_node["prestashop_category"]

    p.fields["tiur"] = raw_product_description
    p.fields["sikum"] = raw_product_sikum

    

    p.fields["img url"] = raw_product_images
    p.fields["img alt"] = raw_product_images_alt

    p.fields["mkt"] = raw_product_mkt_locator
    p.fields["mkt suppl"] = raw_product_mkt_locator
    
    p.combinations["Reference"] = p.fields["mkt"]
    p.combinations["Supplier reference"] = p.fields["mkt suppl"]
    

    price_supplier = price_cleaner.convert_to_float_price(self, raw_product_price_supplier)

    p.fields["mexir lifney"]=price_supplier
    p.fields["mexir olut"]=price_supplier
    p.fields["mexir le yexida"]=price_supplier

    '''

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



    self.p.append(p)

    pass

def product_attributes(self, p, element_delimeter, elements):
    i=0
    skip = False
    c = p.combinations ''' просто сокращенная запись '''
    for e in build_list_from_html_elements(self, element_delimeter, elements):
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

            attr = Formatter.remove_HTML_tags(e)
            ''' первое значение '''
            if c["Attribute (Name:Type: Position)"] == "": c["Attribute (Name:Type: Position)"] = f'''{e.next}:select:0'''
            else: c["Attribute (Name:Type: Position)"] += f''', {e.next}:select:0'''
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




def build_list_from_html_elements(self, element_delimeter, elements) -> []:

    soup : BeautifulSoup = BeautifulSoup(elements , 'html.parser')
    return soup.findAll(element_delimeter)
    #return lst




