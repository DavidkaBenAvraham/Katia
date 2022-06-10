'''
            Функции, присущие поставщику  KSP, которыми я дополняю класс supplier

'''
from logger import Log

from bs4 import BeautifulSoup
import execute_json as json

import sys

import products
from strings_formatter import StringFormatter as SF



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



