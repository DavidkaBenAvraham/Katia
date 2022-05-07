from bs4 import BeautifulSoup
import execute_products

def obrabotaj_polja_tovara(self , p_fields):
    ''' здесь находится логика постобработки '''

    
    soup = BeautifulSoup(self.p['RAW_PAGE_SOURCE'],features="lxml")
    #self.print(f'''soup.title.text =  {soup.title.text} ''')
    self.p['RAW_PAGE_SOURCE'] = ''
    return p_fields

def flush_p(self):
    return product.flush_p(self)
