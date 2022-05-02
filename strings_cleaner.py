from Logging import Log as Log
import re
def remove_unnecessary_words(self,str):
    '''
    престашоп пру импорте 
    принимает не все символы 
    
    '''
    str = clean_string(self,str)

    str = str.replace("'" , "\'")
    str = str.replace('"' , "\"")
    #str = str.replace("'" , " ")
    #str = str.replace('"' , " ")
    str = str.replace('&amp;' , " ")
    str = str.replace('&gt;' , " ")
    str = str.replace('&lt;' , " ")
    str = str.replace('&nbsp;' , " ")
    str = str.replace('&quot;' , " ")
    #str = str.replace(' &amp; ' , " ")
    str = str.replace('#' , " ")
    
    #str = str.replace('כרטיס מסך','')
    #str = str.replace('מחשב נייד','')
    #str = str.replace('נייד','')
    #str = str.replace('לוח אם אינטל למעבד דור 8 ו 9','')
    #str = str.replace('לוח אם למעבדי אינטל דור 10','')
    #str = str.replace('לוח לאינטל דור 10','')
    #str = str.replace('לוח אם אינטל למעבד דור 7','')
    #str = str.replace('לוח אם אינטל','')
    #str = str.replace('לוח אם למעבדי','')
    #str = str.replace('לוח אם למעבד','')
    #str = str.replace('לוח אם','')
    #str = str.replace('מארז ללא ספק','')
    #str = str.replace('מארז וספק','')
    #str = str.replace('מארז למחשב נייח','')
    #str = str.replace('מארז','')
    #str = str.replace('נתב','')
    #str = str.replace('סוויץ','')
    #str = str.replace('מעבד אינטל דור 9','')
    #str = str.replace('מעבד דור 9','')
    #str = str.replace('מעבד אינטל דור 8','')
    #str = str.replace('מעבד דור 8','')
    #str = str.replace('מעבד אינטל דור','')
    #str = str.replace('מעבד דור','')
    #str = str.replace('9 Intel','Intel')
    #str = str.replace('9 intel','Intel')

    #str = str.replace('מקלדת גיימינג','')
    #str = str.replace('סט אלחוטי','')
    
    #str = str.replace('מעבד ללא ליבה גרפית','')
    #str = str.replace('מעבד','')

    #str = str.replace('זכרון למחשב נייד','')       
    #str = str.replace('זכרון למחשב','')    
    #str = str.replace("'","")
    #str = str.replace('כרטיס מסך','')
    #str = str.replace('מסך','')
    #str = str.replace('ספק כוח','')
    #str = str.replace('נייח','')
    #str = str.replace('דיסק קשיח פנימי ל','')
    #str = str.replace('דיסק פנימי','')
    #str = str.replace('דיסק','')
    

    return str
    pass


def cut_field_to_size(self, str, len):
    try:    out_str = str[:len]
    except: out_str = str
    return out_str
    pass

def clean_string(self,str):
    try:
        str = re.sub("^\s+|\n|\r|\s+$", '', str)
        str = re.sub(r'\<[^>]*\>', '', str)
        return str
    except TypeError as ex: #серьезный сбой
        self.log(f''' сбой при очистке строки! 
        {str}  
        ошибка {ex}
        возвращаю как есть''')
        return str

