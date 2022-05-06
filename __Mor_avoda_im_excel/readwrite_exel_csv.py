import pandas as pd
import numpy as np
from xlrd import XLRDError #<- отлавливаю ошибки xlrd (excel reader)
#from decimal import Decimal # <- округления чисел https://metanit.com/python/tutorial/6.4.php
from decimal import Decimal
#
#


def convert_Morlevi_to_csv(date = None):
    '''
    date = DD-MM-YY

Mехирон по страницам экспортирую в отдельные файлы csv 
    data\\(нужная страница).csv - экспортированый из файла морлеви лист
    формат: [sheet]_DD-MM-YY.csv

Названия страниц в файле МорЛеви
sheets:
notebooks
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
остальное по ходу пьесы
'''

    # кортеж страниц в книге морлеви
    #### ВНИМАНИЕ!!!
    #   могут быть пробелы после названия листа. Например: 'Peripheral '
    sheets = ['Notebook | Tablets',
              'MB',
              'CPU',
              'Memory',
              'VGA',
              'LCD | TV',
              'HDD | SSD | DVDRW ',
              'Cases',
              'PSU',
              'Peripheral ',
              'Printers',
              'Network']
   
    morlevi_file = 'data\\mor-levi_'+ date +'.xls'

    ##############################################################
    #           читаю каждую страницу мехирона
    #           через цикл 
    ##############################################################
    for sheet in sheets:
        sheet2save = str(sheet).replace(' | ','_').strip()
   #try:
        df = pd.read_excel(open(morlevi_file , 'rb'), sheet_name=sheet) # doctest: +SKIP
        ########################################
        #                обрабатывю
        ########################################

# 1         Переименовываю колонки
        try:
# 1.1       # переименовывааю в "Price"
            # если колонка цена названа "Price $" или есть пробел
            df.rename(columns={'Price $':'Price'}, inplace=True)
            df.rename(columns={'Price $ ':'Price'}, inplace=True)
            df.rename(columns={'Price ':'Price'}, inplace=True)
            df.rename(columns={'      ':'P/N','Unnamed: 3':'Price'}, inplace=True)
# 1.2        --//--   זמינות 
            df.rename(columns={'זמינות':'zminut'}, inplace=True)
            df.rename(columns={' זמינות':'zminut'}, inplace=True)
            df.rename(columns={'זמינות ':'zminut'}, inplace=True)


        except Exception:
            self.log('колонка НЕ переименовалась  - ' + sheet)
            self.log(str(Exception))
            self.log(df.columns)

# 2    убираю не релавантвые мусорные строки.
#      Пробелы, пустые значения, call и т.п. в ячейках
#      заменяю на  NAN, а потом вытираю строку с NAN в ячейке
       # try:
# 2.1       чищу колонку Price заменой мусора на Nan
        df['Price'].replace('', np.nan, inplace=True)
        df['Price'].replace(' ', np.nan, inplace=True)
        df['Price'].replace('-', np.nan, inplace=True)
        df['Price'].replace('call', np.nan, inplace=True)
        df['Price'].replace('Price $', 'Price', inplace=True)

        df.dropna(subset=['Price'], inplace=True) # убираю строки без цены
        self.log(df.Price)
# 2.2       чищу колонку זמינות  заменой חסר / call на Nan
        df['zminut'].replace('חסר', np.nan, inplace=True)
        df['zminut'].replace(' חסר', np.nan, inplace=True)
        df['zminut'].replace('חסר ', np.nan, inplace=True)
        df['zminut'].replace('call', np.nan, inplace=True)

        df.dropna(subset=['zminut'],inplace=True) # убираю строки חסר / call

        if sheet2save == 'Notebook_Tablets':
            df['CPU'].replace('', np.nan, inplace=True)
            df.dropna(subset=['CPU'],inplace=True) # убираю строки без процессора
            
            

        #except Exception as e:
        #    self.log(sheet)
        #    self.log(e)
        #    self.log('Не почистилось')
        #    self.log(df[sheet])
# 3        ##############################################################
        #                   выставляю продажную цену
        #                   умножая всю колонку на coefficient 
        #                   и добавляю колонки 'ML' ; 'ML + VAT'
        ##############################################################
        coefficient = 1.12 
        vat = 1.17
 
        '''
        работает любой способ 
        df.Price *=1.4
        df.Price = df.Price*1.4
        df.Price = df.Price.multiply(1.4)
        df['Price'] = df['Price']*1.4
        df.loc[:, 'Price'] *=1.4
        df.iloc[:, 1] = df.iloc[:, 1]*1.4 
                    ^-  индекс столбца
        '''
        try:
            df['ML'] = df.Price # <- МорЛеви
            df['ML + VAT'] = df.Price * vat # <- מע''מ
            df.Price *= coefficient # <- клиенту


            #       Красивая кругленькая цена
            ################################################################
            # 1. делим на 100, чтобы получить из 1234 12.34
            # 2. окрукгляем до ближайшего большего 12.4
            # 3. умножаем на 100, получаем 1240
            ################################################################

            #округляю
            df.Price = round(df.Price)

            #1.
            df.Price /= 10

            #2.
            df.Price = round(df.Price)

            #3.
            df.Price *= 10

            flag_ok2write = True # всё ок, можно писать в выходной файл
        except Exception as e:
            self.log('ошибка пересчета цены')
            self.log(e)
                
            self.log(sheet + ' - не удалось изменить цену!')
            self.log(df.Price)
            flag_ok2write = False # нельзя записывать файл



        if flag_ok2write: # можно писать файл
            try:# ####################################
            #               пишу
            #######################################
            #   #
                # НОУТБКИ 
                #
                if sheet2save == 'Notebook_Tablets':
                    
                    ## По МКТ ДЕЛАЕМ КОЛОНКУ С ФИРМОЙ
                    # цикл строк датафрейма
                    for index, row in df.iterrows():
                        if str(row['P/N']).startswith('ASN'):
                            df.at[index, 'MNF'] = 'ASUS'  ###df.at == df.loc
                        if str(row['P/N']).startswith('HP'):
                            df.at[index, 'MNF'] = 'HP'  ###df.at == df.loc
                        if str(row['P/N']).startswith('LNN'):
                            df.at[index, 'MNF'] = 'LENOVO'  ###df.at == df.loc
                        if str(row['P/N']).startswith('DLN'):
                            df.at[index, 'MNF'] = 'DELL' ###df.at == df.loc

                    cols2save = ['MNF','P/N',
                                'Family',
                                'Model',
                                'Color',
                                'Screen',
                                'CPU',
                                'HDD',
                                'RAM',
                                'OS',
                                'Graphic',
                                'Resolution',
                                'ODD',
                                    'Price'                                    
                                    'ML',
                                    'ML + VAT']

                # переделываю имя листа в морлеви в нормальное имя файла
                csv_file = 'data\\' + str(date) + '_' + sheet2save + '.csv'
                df.to_csv(csv_file, encoding='utf-8', columns = cols2save) # <=> df[['P/N','Price']].to_csv(csv_name, encoding='utf-8')
                self.log('-== ' + csv_file + ' записан OK! =-')
            except FileNotFoundError:
                self.log("File not found")
            except PermissionError:
                self.log("Файл открыт!!!")
                self.log(csv_file)
            except Exception as e:
                self.log("Файл не записался!!!")
                self.log(df.columns)
                self.log(csv_file)
        else: # нельзя записывать!
            self.log('-== НЕ записан!!!! - ' + csv_file + ' =-')
            self.log()

    ###### обработчики ошибок открытия файлов МорЛеви ексель
    #except XLRDError as e: # скорее всего не найден лист (м.б. пробелы?)
    #    self.log(e)
    #    self.log(sheet + '\n######### скорее всего не найден лист (м.б. пробелы?) #########\n')
    #    #sys.exit(-1)
    #except Exception as e: # вааще хуй знает чё за ошибка
    #    try: # и как ее, блядь, парсить
    #        self.log(sheet + ' -= e.message  =- ')
    #        self.log(e.message)
    #    except:   
    #        self.log(sheet + '\n -=  вааще хуй знает чё за ошибка =- n')
    #        self.log(e)
    #        self.log(df.columns)



    self.log('OK')
    pass



# читаю из файла csv
#  
def get_csv_data(csv_file = None, cols = None, names = None):
    '''
    cols - колонки, релевантвые 
    запрашиваемой порции данных из файла

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

    '''
    file = 'data\\'+ csv_file +'.csv'
    # с определенными колонками
    # return pd.read_csv(file, usecols=cols)
    # return pd.read_csv(file, names=cols)
    # все колонки
    return pd.read_csv(file, usecols = cols, names = names)

