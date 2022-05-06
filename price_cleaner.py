import math
import re
import strings_cleaner

 # https://all-python.ru/osnovy/okruglenie.html
def convert_to_float_price(self ,price: str) -> float:
    '''
    если на сайте поставщика нет цены 
    вернется False
    '''
    if price == False or price == None or price == '': return float(-1)
    else:
        price = ___clean_price(self,str(price))
        if price == '': return -1
        else:
            try:
                return float(price)
            except:
                self.log( f''' price не число! Гляди: {price} ''')
                return float(-1)
            


def ___clean_price(self ,price:str) -> str:
    price = strings_cleaner.remove_unnecessary_words(self ,price)
    price = price.replace('₪' , "")
    price = price.replace(' ' , "")
    price = price.replace(',' , "")
    price = price.replace('$' , '')

    #try:
       

    #    self.log( f''' После преобразований цена = {price}''')
    #    p_ = ''
    #    for x in price: 
    #        p_ = p_ + uberi_tohku_i_nuli_posle(self, str(x)) # Собираю цену из словаря
    #        self.log( f''' Собираю цену  p_={p_} ''')
    #    price = p_
    #    self.log( f''' После второго преобразования цена = {price}''')
    #except Exception as ex:
    #    self.log( f''' Ошибка: {ex} 
    #    price = {price}''')
    #    if str(type(price)).find('list') >-1: 
    #        try:
    #            self.log( f''' Ой! цена = {price} ''')
    #            price = price[0]
    #            self.log( f''' А сейчас = {price} ''')
    #        except:
    #            self.log(f''' Проблема с получением цены. Она выглядит так: {price} !!! Будет  ХУЙ ! 
    #            Проверь цену {price}
    #            type {str(type(price))}''')
    #            return float(-1)
    #if price == None or price == '' : return 0

    #self.log( f''' Начинаем чистить цену {price} ''')
    #price = price.replace('₪' , '')
    #price = price.replace('$' , '')
    #price = price.replace(',' , '')
    
    #price = price.replace(' ' , '')
    ##price = price.split()
    #self.log( f''' почистили {price} ''')
    return price


def okrugli_krasivo(price):

    #       Красивая кругленькая цена
    ################################################################
    # 1. делим на 100, чтобы получить из 1234 12.34
    # 2. окрукгляем до ближайшего большего 12.4
    # 3. умножаем на 100, получаем 1240
    ################################################################

    #округляю
    price = round(price)

    #1.
    price /= 10

    #2.
    price = round(price)

    #3.
    price *= 10

    if price < 10 : price =10

    return price

def uberi_tohku_i_nuli_posle(self , price_s_tohkoj:str) -> str:
    p_ = price_s_tohkoj.split('.')
    self.log( f'''Убрал точку с нолями после нее 
    Получил: {price_s_tohkoj}
    Отдал: {p_[0]} ''')
    return p_[0]
    pass
