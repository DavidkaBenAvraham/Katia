# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia.Tools
## Documentation for module strings_formatter.py
    #
    #        $a = '1,5,';
    #        if(!preg_match('/^(?:\d\,)+$/', $a)) {
    #         echo 1;
    #        }
    #        ^ - начало строки
    #        $ - конец строки
    #        (?:\d\,) - цифра и запятая
    #        + - ищем один или более раз (в данном случае цифру с запятой)
    #        Если нужно искать без запятой в конце:
    #        /^(?:\d\,)+\d?$/
    #        Если через запятую будут указаны большие числа (132,564,234324):
    #        /^(?:\d+\,)+\d?$/
    #    наиболее важные методы регулярного выражения модуля Python Re:
    #                Re.findall (шаблон, строка) : Проверяет, соответствует ли строка шаблон и возвращает Все вхождения 
    #                                            сопоставленного шаблона как список строк.
    #                Re.Search (шаблон, строка) : Проверяет, соответствует ли строка шаблона Regex и возвращает только Первый матч 
    #                                            как объект матча. Объект Match – это просто: объект, который хранит мета информацию о матче, 
    #                                            такой как соответствующая позиция и соответствующая подстрока.
    #                Re.match (шаблон, строка) : Проверяет, если кто-нибудь Струнный префикс 
    #                                            Соответствует шаблону Regex и возвращает объект совпадения.
    #                Re.fullmatch (шаблон, строка) : Проверяет, если целая строка Соответствует шаблону Regex и 
    #                                            возвращает объект совпадения.
    #                Re.compile (Pattern) : Создает объект регулярного выражения из шаблона для ускорения совпадения, 
    #                                            если вы хотите использовать шаблон Regex несколько раз.
    #                Re.Split (шаблон, строка) : Разбивает строку, где бы закономерность регенсирует и возвращает список строк. 
    #                                                Например, вы можете разделить строку в список слов, используя пробельные символы в качестве сепараторов.
    #                Re.sub (шаблон, репрект, строка) : Заменяет ( sub stitutes) Первое возникновение рисунка Regex с заменой 
    #                                                String Repland и вернуть новую строку.
    #                чтобы проверить, содержит ли строка шестнадцатеричные цифры (от 0 до 9 и от A до F), следует использовать 
    #                такой диапазон:
    #                [A-Fa-f0-9]
    #                Чтобы проверить обратное, используйте отрицательный диапазон, который в нашем случае подходит под любой символ, 
    #                кроме цифр от 0 до 9 и букв от A до F:
    #                [^A-Fa-f0-9]


    ##pattern_find_phone : re = attrib(init = False , default = re.compile(r'''(
	   ## (\d{3}|\(\d{3}\))?   #Area code
	   ## (\s|-|\.)			 #Separator
	   ## (\d{3})				 #First 3 digits
	   ## (\s|-|\.)			 #Separator
	   ## (\d{4})				 #Second four digits
	   ## (\s*(ext|x|ext.)\s*(\d{2,5}))?
	   ## )''', re.VERBOSE)

    ##pattern_find_email : re = attrib(init = False , default = re.compile(r'''(
	   ## [a-zA-Z0-9_%+-.]+	#Username
	   ## @					#@ symbol
	   ## [a-zA-Z0-9.-]+		#domain name
	   ## (\.[a-zA-z0-9]{2,5})#dot-something
	   ## )''', re.VERBOSE)


import re
import pandas as pd
import execute_json as json
import sys
import os
import importlib
import datetime
import time
import json
import random as rnd

from attr import attrs, attrib, Factory

'''
https://github.com/chuanconggao/html2json/blob/master/README.md
'''


pattern_remove_HTML :re = re.compile ('<[^<]+?>')
pattern_remove_non_latin_characters : re = re.compile ('^[A-Za-z0-9]*')
pattern_remove_line_breaks : re = re.compile ('^\s+|\n|\r|\s+$')
pattern_clear_price : re = re.compile ('[^0-9.,]')
pattern_clear_number : re = re.compile ('[^0-9.]')
pattern_remove_special_characters :re = re.compile ('[#|]')            
pattern_remove_supplier_name :re = re.compile ('[KSP,ksp]')
    

@attrs
class StringFormatter():
    ''' Обработчик строк '''

    def remove_suppliers_and_special_chars(method_to_decorate:object , s:str)->object: 
        ## Декоратор для внутренних функций форматера.
        #Убираю имя поставщика и значки не удовлетворяющие условиям хранения строк в базе данных
        #моего каталога
        
        def remover(self , s:str)->str:
            s = pattern_remove_suppliers_from_string.sub(r'',s)
            s = pattern_remove_special_characters.sub(r'',s)
            s = pattern_remove_line_breaks.sub(r'',s)
            method_to_decorate(self,s)
        return remover(s)

    
    def __attrs_post_init__(self , *srgs, **kwrads):
        ## инициализация класса StringFormatter()
        self.pattern_remove_HTML = pattern_remove_HTML
        self.pattern_remove_non_latin_characters = pattern_remove_non_latin_characters
        self.pattern_remove_line_breaks = pattern_remove_line_breaks
        self.pattern_clear_number = pattern_clear_number
        self.pattern_clear_price = pattern_clear_price
        self.pattern_remove_special_characters = pattern_remove_special_characters

        pass

    # убираю все значки переноса строк
    def remove_line_breaks(self,s:str)->str:
        def _(s):
            return self.pattern_remove_line_breaks.sub(r' ', s).strip()

        if isinstance(s , list ):
            for sub_s in s:
                sub_s = _(sub_s)
        else: s=_(s)

        return s
        


    #@remove_suppliers_and_special_chars
    def remove_htmls(self , s):
        def _(s):
            return self.pattern_remove_HTML.sub(r' ', str(s)).strip()

        if isinstance(s , list ):
            for sub_s in s: sub_s = _(sub_s)
        else: s=_(s)
        return s


    def remove_special_characters(self , s:str)->str:
        s = self.remove_htmls(s)
        s = self.remove_line_breaks(s)
        return s


    def clear_number(self , s):
        def _(s):
            s = self.pattern_clear_number.sub(r'', str(s)).strip()
            return s

        if isinstance(s , list):
            for sub_s in s: sub_s = _(sub_s)
        else: s = _(s)
        return s

    def clear_price(self , s):
        def _(s):
            s = self.pattern_clear_price.sub(r'', str(s)).strip().replace(',','.')
            return s

        if isinstance(s , list ):
            for sub_s in s: sub_s = _(sub_s)
        else: s=_(s)
        return s

      
