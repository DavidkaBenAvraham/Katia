from Logging import Log as Log
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


def pull_products_details_from_blocks(self , products_blocks):
    
    '''
    https://stackoverflow.com/questions/34301815/understand-the-find-function-in-beautiful-soup#_=_
    Here we are also checking for presence of data-value attribute.
    soup.find("span", {"class": "real number", "data-value": True})['data-value']
    '''

    #всегда в супе лист блоков
    try:
       
        for block in products_blocks:
            url = find_link_to_full_product_page(block)
            soup = BeautifulSoup(block, 'lxml')
            extract_product_from_soup(self, soup)
            
        return True
    except Exception as ex:
        self.log( f''' Ошибка 
        {ex}
        при чтения блока товара 
        {products_blocks}''')
        #sys.exit()


def find_link_to_full_product_page(self,block):
    print(block)
    pass

def extract_product_from_soup(self, soup):
    try:
        div = soup.find(['div'])
        a = soup.find('a', attrs={'class':'MuiTypography-body1'})
        
        

        imgs = soup.find_all('img')
        spans = soup.find_all('span')
        divs = soup.find_all('div')
        pp = soup.find_all('p')
        aa = soup.find_all('a')

        print(aa)


        #if str(type(spans)).find("None") >-1:spans = pp
        
        _mkt = False
        for span in spans:
            if span.has_attr('data-id'):
                mkt = str(span.text).split(':')[1]
                break



        _title = soup.find('span',attrs={'class':'MuiTypography-root.MuiTypography-body1'})
        _supplier_price = soup.find('span', attrs = {"aria-label":"שקלים"}).previous_sibling
        _supplier_price = rgf.clean_price(_supplier_price)
        _shop_price_string = f'''{_supplier_price}{self.price_rule}'''
        _shop_price = eval(_shop_price_string) 
        
        #for p in pp:
        #    for attr in p.attrs:
        #         self.log(f''' p.attr {attr}''')
        #         self.log(f''' {p.attrs[attr]}''')
       
        #    self.log('------------------------')

        for a in aa:
            if a.has_attr('aria-label') and str(f'''{a.attrs['href']}''').find(f'web/item')>-1:
                _title = str(a.attrs['aria-label'])
                break
        

        img = ''
        for img in imgs:
            #self.log(f''' IMG - ''')
            #self.log(img.has_attr('alt'))
            if img.has_attr('alt') and str(f'''{img.attrs['alt']}''').find('הטבה מיוחדת')>-1:continue
            if img.has_attr('src') and str(f'''{img.attrs['src']}''').find(f'https://ksp.co.il/shop/items')>-1:
                img = img.attrs['src']
                break
     
    
        self.p = dict(self.fields)
        self.p['id'] = mkt

        self.p['categories'] = str(f'{str(self.current_node["prestashop_category"])}')
        
        self.p['title'] = rgf.clean_string_retun_only_latin_and_numbers(_title)
        
        self.p['sikum'] = _title
        self.p['brand'] = self.current_node["brand"]
        self.p['mexir lifney'] = _supplier_price
        self.p['mexir olut'] = _shop_price
        #self.p['Reference'] =  self.p['title']
        self.p['mkt'] = mkt
        self.p['mkt suppl'] = mkt
        self.p['sikum'] = f'''{_title}'''
        self.p['img url'] = img
        self.p['img alt'] = str(f'''{self.p['brand']} {self.p['title']}''')
        self.p['koteret meta'] =  self.p['title']
        self.p['rewrie url'] = self.p['title'].strip().replace(" ","-").replace("&","_")
        
        #self.p['maafianim mufradim bpsik'] = str(f'{str(self.current_node["properties"])}').replace("{","").replace("}","").replace('"','')


        self.products_list.append(self.p)


        


    except Exception as ex:
        self.log( f''' Ошибка при напонении полей словаря товаров 
        {ex}''')
        #self.log( f''' Поля товара 
        #{p_fields}''')
        #sys.exit()
        return self,False
     