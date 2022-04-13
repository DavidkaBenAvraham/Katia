import pandas as pd
#
#   data\\нужная страница.csv - экспортированый из Гугл таблиц файл
#
sheets =  ['laptops']

file_csv = 'data\\'+sheets[0]+'.csv'

# чтение данных из файла 
#  
def get_csv_data(sheet = None, header=None, cols = None):
    '''
    cols - колонки, релевантвые 
    запрашиваемой порции данных из файла

    '''
    file_csv = 'data\\'+sheets[sheet]+'.csv'
    return pd.read_csv(file, usecols=cols)

