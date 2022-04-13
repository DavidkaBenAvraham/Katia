import execute_products as product
from Ini import Ini
#import execute_json as jsn
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

    #1. Общий список товаров полученный в ходе выполнения ВСЕХ сценариев
    self.p = []


    for scenario_files in self.scenaries:
        
        for json_file in scenario_files:      
            
            self.scenaries = jsn.loads( f'''{self.root}\\Ini\\{json_file}''')

            # заполняемый сейчас список товаров
            current_p = run_scenario(self)
            #self.log(f''' список заполненных товаров current_p {current_p}''')
            # проверяю, что список товаров не пустой и присоединяю его к существующшму
            if not check_type.is_none_or_false(current_p):  
                self.p += current_p

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
        - <properties> - свойства товара: цпу, экран, гарантия итп
        '''
        self.current_node = self.scenaries[scenario_node]

        product.build_produscts_list_by_scenario(self)


    product.flush_p(self)
