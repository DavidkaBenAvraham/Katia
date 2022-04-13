# 'https://www.facebook.com/groups/216589205370098/?fref=nf' Рамат Ган
# 'https://www.facebook.com/groups/473713946160027'  бат Ям
# 'https://www.facebook.com/groups/petahtikva.ads' Петах Тиква
# 'https://www.facebook.com/groups/1684305088524622' Нетания

# ожидания
#from selenium.webdriver.support import expected_conditions as EC
#https://selenium-python.readthedocs.io/waits.html
#wait = WebDriverWait(driver, 10)
#element = wait.until(EC.element_to_be_clickable((By.ID, 'someid')))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from pathlib import Path, PureWindowsPath
import datetime
from os.path import abspath

from messages_log import Logging
import csv_executor




def upload_img(driver , wait):
    upload_input_class = '_n._5f0v'
    
    element = wait.until(EC.element_to_be_clickable((By.NAME, 'xhpc_message_text')))
    path2file = abspath(__file__)[:abspath(__file__).rfind('\\')]+'\\imgs\\800px-Shabbat_Candles.jpg'
    path2file = Logging.path +'\\imgs\\800px-Shabbat_Candles.jpg'
    driver.find_element_by_class_name(upload_input_class).send_keys(path2file)
    

def send_2_groups(driver , msg , lng='ru' ):

    df = csv_executor.get_groups(lng)


    pict_num = 0
    pict = ['hag-pesah-sameah.jpg',
            '135833.png',
            '135327.png',
            '13882.png',
            '1850ukr_pesah.jpg',
            'A_Seder_table_setting.jpg',
            'pesah1.jpg']
   

    wait = WebDriverWait(driver, 20)
    logging = Logging()
    for g in df['url']:
    
            driver.get(g)
            '''
            <textarea class="_4h98 navigationFocus" placeholder="כתוב משהו..." 
                name="xhpc_message_text" id="js_1d"></textarea>
            '''
            try:
                element = wait.until(EC.element_to_be_clickable((By.NAME, 'xhpc_message_text')))
                element.click()
                driver.execute_script("window.scrollBy(0,200)")
                element.send_keys(msg)
    #######################################  kartinki
                upload_img(driver , wait)
    #############################################


                btn_send_css_name = "_1mf7._4jy0._4jy3._4jy1._51sy"    
                element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, btn_send_css_name)))
                #element.click()

            
                ########### добавляю в список успешно отправленное сообщение
                logging.success_log(driver.current_url, driver.title)
            except TimeoutException:
                logging.error_log(driver)
                pass

    logging.write_success()


from selenium.common.exceptions import NoSuchElementException
# https://www.pingshiuanchua.com/blog/post/error-handling-in-selenium-on-python

def find_element_by_(by, driver):
    try:
        pass
    except:
        pass
    pass