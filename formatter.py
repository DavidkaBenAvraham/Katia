import re
import pandas as pd
import json
import sys
import os
import importlib
import datetime
import time

class Formatter():
    '''
            $a = '1,5,';
            if(!preg_match('/^(?:\d\,)+$/', $a)) {
             echo 1;
            }
            ^ - начало строки

            $ - конец строки

            (?:\d\,) - цифра и запятая

            + - ищем один или более раз (в данном случае цифру с запятой)

            Если нужно искать без запятой в конце:
            /^(?:\d\,)+\d?$/

            Если через запятую будут указаны большие числа (132,564,234324):
            /^(?:\d+\,)+\d?$/

    '''
    pattern_remove_HTML :re = re.compile ('<[^<]+?>')
    pattern_remove_non_latin_characters : re = re.compile('^[A-Za-z0-9]*')
    pattern_remove_line_breaks : re = re.compile('^\s+|\n|\r|\s+$')
    pattern_clear_price : re = re.compile('[^0-9.]')
    pattern_remove_special_characters :re = re.compile('^[\|,ksp,KSP,\#]+$')
    pattern_remove_suppliers_from_string :re = re.compile('[^KSP,ksp]+$')
#  
    @Formatter.remove_suppliers
    def get_now(self,strformat = '%YY-%MM-%d %H:%M:%S') -> datetime:
        return datetime.datetime.now().strftime(strformat)

    def remove_line_breaks(self,str:str)->str:
        return self.pattern_remove_line_breaks.sub(r' ', str)

    def remove_HTML_tags(self,string_HTML:str)->str:
        ''' Удаляю HTML из строки'''
        return self.pattern_remove_HTML.sub(r' ', str(string_HTML))

    def remove_special_characters.sub(str:str)->str:
        return self.pattern_remove_special_characters(r' ', str)


    
    def clear_price(self, str:str)->str:
        return self.pattern_clear_price.sub(r'',str)

    def check_int(self, data) -> bool:
        if isinstance(data, int) : return True
        else: return False

    def check_bool(self, data) -> bool:
        if isinstance(data, bool) : return True
        else: return False

    def check_none_or_false(self, data = False) -> bool:
        if isinstance(data, bool) and data == False: return True
        if data == None: return True
        else: return True



#import re

##https://docs.python.org/3/library/re.html
##https://ru.stackoverflow.com/questions/169472/%D0%A0%D0%B5%D0%B3%D1%83%D0%BB%D1%8F%D1%80%D0%BD%D0%BE%D0%B5-%D0%B2%D1%8B%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE-%D0%BB%D0%B0%D1%82%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B5-%D0%B1%D1%83%D0%BA%D0%B2%D1%8B-%D0%B8-%D1%86%D0%B8%D1%84%D1%80%D1%8B

#pattern_remove_non_latin_characters = re.compile('^[A-Za-z0-9]*')

#'''
#https://ru.stackoverflow.com/questions/575862/%D0%A0%D0%B5%D0%B3%D1%83%D0%BB%D1%8F%D1%80%D0%BD%D0%BE%D0%B5-%D0%B2%D1%8B%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B4%D0%BB%D1%8F-%D1%87%D0%B8%D1%81%D0%B5%D0%BB-%D1%81-%D0%BF%D0%BB%D0%B0%D0%B2%D0%B0%D1%8E%D1%89%D0%B5%D0%B9-%D1%82%D0%BE%D1%87%D0%BA%D0%BE%D0%B9

#^[0-9]*[.,]?[0-9]+$
#           ^
#См. демо

#^ - начало строки
#[0-9]* - 0 и более цифр
#[.,] - точка или запятая ([,.]? - одна или ноль запятых или точек)
#[0-9]+ - 1 и более цифр
#$ - конец строки.

#'''
#pattern_price = re.compile('^[0-9]*[.,]?[0-9]+$')


#def clean_string_retun_only_latin_and_numbers(str):
#    str = remove_non_latin_charcters(str)
#    #str = remove_line_breaks(str)
#    #str = remove_html_tags(str)
#    return str

#def clean_price(str):
#    m =  pattern_price.search(str)
#    return m.group().replace(",",".").replace(".","")

## Удаляю все, кроме латиницы
#def remove_non_latin_charcters(str):
#    #m = pattern_remove_non_latin_characters.findall(str)

#    #outs = ''.join(re.findall('[A-Za-z0-9 ~!@$%^&*()-=+]', str))
#    return ''.join(re.findall('[A-Za-z0-9 ~!@$%^&*()-=+#]', str)).replace('#',' ').strip()

#def remove_line_breaks(str):
#    return re.sub("^\s+|\n|\r|\s+$", '', str)
 
#def remove_html_tags(str):
#    #https://stackoverflow.com/questions/11229831/regular-expression-to-remove-html-tags-from-a-string
#    return re.sub('<[^>]*>' , str)

