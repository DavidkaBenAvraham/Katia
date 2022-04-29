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
