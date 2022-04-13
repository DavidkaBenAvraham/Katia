import pandas as pd
import readwrite_exel_csv as csv
from decimal import Decimal 


def get_data_from_csv(csv_file = None, sheet = None, date = None, cols = [0,3], names = ['id','price']):
    '''
    cols - колонки, релевантвые 
    запрашиваемой порции данных из файла
    например, cols = [0,3] для Морлеви; cols = [0,2] для сайта
    names - имена присваевыемые для создания датасета [id, price]

       sheet - 
           laptops
           mb
           cpu
           memory
           vga
           monitors
           mb
           hdd
           cases
           psu
           printers

        date - DD-MM-YY
    '''
    if csv_file == None:
        csv_file = str(sheet) + '_' + str(date)
    pass
    
    self.log(csv_file)

    data = csv.get_csv_data(csv_file = csv_file , cols = cols , names = names).dropna(how ='any')
    return data
    pass

def concat(df1, df2):
    result = concat([df1,df2]).drop_duplicates(keep=False)
    return result
    pass


def stock_changes(csv_products_by_category, date_new, date_old, store_sheet = None):
    '''
    format date = dd-mm-yy
    csv_products_by_category - файл распарсенный из мехирона морлеви в 
    функции    convert_Morlevi_to_csv(date)
    '''
    df_new = get_data_from_csv(csv_file = str(date_new) + '_' + str(csv_products_by_category), cols = [1,2], names = ['id','price'])
    df_old = get_data_from_csv(csv_file = str(date_old) + '_' + str(csv_products_by_category), cols = [1,2], names = ['id','price'])
    df_store = get_data_from_csv(csv_file = store_sheet , cols = [1,2], names = ['id','price'])

    #For "IN" use: something.isin(somewhere)
    #Or for "NOT IN": ~something.isin(somewhere)
    new_arrivals = df_new[~df_new.id.isin(df_old.id)] # новые НЕ содержащие старые
    came_out = df_old[~df_old.id.isin(df_new.id)] # старые НЕ содержащие новые

    self.log('\n\n----------- Цены пересчитаны в продажные  ---------------')
    self.log('################## --- Появились новые --- #############################')
    self.log()
    self.log(new_arrivals)
    self.log()
    self.log('################## --- Ушли старые --- #################################')
    self.log()
    self.log(came_out)
    self.log()

    df_merged = pd.merge(df_old, df_new ,  on = 'id')
    price_changed = df_merged[df_merged.price_x != df_merged.price_y]

    self.log('################## --- Изменилась цена --- #################################')
    self.log()
    self.log(price_changed)

    self.log('################## --- Сайт --- #################################')

    # парсим датафрейм магазина по строкам 
    # в поисках изменний цены
    self.log('Изменилась цена')
    for index, row in df_store.iterrows():
        # ищем строку в датасете морлеви
        # строка состоит из row['id']; row['price']
        find_mkt(row , df_new)
    pass
    # парсим датафрейм магазина по строкам 
    # в поисках ушедших товаров
    self.log('Убрать с сайта')
    for index, row in df_store.iterrows():
        # ищем строку в датасете морлеви
        # строка состоит из row['id']; row['price']
        find_mkt(row , came_out)
    pass

# в базе даннных магазина ищем мкт из морлеви
def find_mkt(raw_whatfind , df_wherefind):
    for index, row in df_wherefind.iterrows():
        flag = False
        # метод find() 
        # ищет подстроку в строке
        if str(raw_whatfind['id']).find(str(row['id'])) != -1:
            flag = True
            self.log(' = > ' + raw_whatfind['id'] + 
                  ' цена на сайте: ' + raw_whatfind['price'] +
                  ' цена мор леви  ' + row['price'] )
    if ~flag:
        #self.log('есть на сайте, нет в мор ' + raw_whatfind['id'])
        pass
    pass

def convert_Morlevi_to_csv(date = None):
    'date format: dd-mm-yy'
    csv.convert_Morlevi_to_csv(date)
    pass
#if __name__ == "__main__":
#    # execute only if run as a script
#    main()
