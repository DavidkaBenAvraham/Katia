

from Driver import Driver 
from ini_files import Ini
from logger import Log
import execute_json as jsn
import execute_scenaries as execute_scenaries


class Dornet(Driver):
    def __init__(self, **kwards): 
        self.supplier_name = 'dornet'
        self.log = Log(self.supplier_name)
        super().__init__(**kwards)
        self.self.supplier = jsn.load('dornet.json')
        self.supplier_prefics = self.self.supplier["supplier_prefics"]
        self.supplier_name = self.self.supplier["supplier_name"]
        self.price_rule = self.self.supplier["price_rule"]
        #self.num_items_4_flush = self.self.supplier["num_items_4_flush"]
        self.scenaries = self.self.supplier["scenaries"]
        #локаторы логин
        self.locators['login'] = jsn.load('dornet_login.json')
        #локаторы элементов страницы
        self.locators = jsn.load('dornet_locators.json')
        self.json_infinity_scroll = self.self.supplier["infinity_scroll"]
        #Бренды
        self.brands = jsn.load('brands.json')['brand']
        
        #Имя текущего файла экспорта CSV
        self.filename_for_export_data = ''

        #self.print(f'''запустился класс dornet''')
           
        self.ps_list = []

    

    def run(self):
        self.get_url('https://www.cable.co.il/')
        if login.log_f_in(self): return self
        else: return False
    
    def fill_df_products_by_scenaries(self , scenario_files ='' ):
        p = execute_scenaries.execute_list_of_scenaries(self,scenario_files)
        return product.flush_p(self , p)

    def obrabotaj_polja_tovara(self , p_fields):
        return product.obrabotaj_polja_tovara(self , p_fields )

  