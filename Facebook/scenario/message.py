from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import *

import datetime
import time
import sys
from logger import Log
 
import Facebook.db as fb_db
import Messages.db as msgs_db

from ini_files import Ini
import Facebook.scenario.message_controllers as controllers




def send_single_message_into_many_groups(self , msg_id = -1 , sug = '*',  from_ROWID = 0 , to_ROWID = 'max'):
        '''
        Рассылатель сообщений в группы Фейсбук

        Одно сообщение в множество групп
        '''

         # 1. вытаскивем группы из базы данных
        fb_groups = fb_db.get_fbgroups(lang = self.get_current_lang() , msg_id = msg_id,
                                      from_ROWID = from_ROWID , to_ROWID = to_ROWID) 
            
        '''
         --== сюда можно засунуть логику обработки =-

        из таблицы групп по одному языку и типу группы
        получаю датафрейм групп на этом языке

        '''

        for index , row in fb_groups.iterrows():
            fbgroup_id = row['ROWID']
            fbgroup_url = row['url']
            self.print(f"Старт рассылки {msg_id} в группу {fbgroup_id}")
            status = False
            if send_single_message_into_one_group(self , msg_id , fbgroup_id, fbgroup_url): # пишу в одну группу
                if controllers.button_send_click(self): status = True
                else: status = False
           
            msgs_db.log_status_sent_message_2fbgroup(self, msg_id , fbgroup_id, status) # логгирование в бд
            return status


def send_single_message_into_one_group(self , msg_id, fbgroup_id = -1,  fbgroup_url = ''):
    '''
    пишу сообщение только в одну группу
    '''
    #msg = msgs_db.get_one_message(self , msg_id)
    if self.get_url(fbgroup_url)   :            # 1) открываю страницу группы
        '''
        может возникнуть ситуация, когда я не вошел через логин и 
        или потерялась сессия или что-то другое. 
        Я проверяю, и если на странице есть поля "email" и "pass"
        повторяю сценарий логин

        код проверки логина
        '''
        #self.check_login()

        #self.bitul_atraot_mi_daf_FB() # отменяю получение сообщений из группы


        self.driver.execute_script("window.scrollBy(0,200)") # поднял окошко
                
        # 1) Click кнопка начала записи сообщения
        self.log("Клик по кнопке для начала записи")
        if controllers.btn_start_writting_message_click(self) == False:
            self.log("Не нажалась кнопка начала записи сообщения")
            return False

        # 2) Click на поле для открытия ввода
        self.log("Клик для переноса фокуса")
        if controllers.textarea_before_message_focus(self) == False:
            self.log("Не перевелся фокус на поле ввода сообщения")
            return False
        #3) 
        if self.current_message["message"] != "" : # текстовое сообщение
            self.log("Инсерт текста сообщения  -------- ")
            if write_message(self, self.current_message["message"]) == False:
                self.log("Не удалось записать сообщения")
                return False
       
        if self.current_message["message_images_names"] != "" : # картинка
            self.log("Начинаю аплоад картинки")
            if upload_img(self, self.current_message["message_images_names"]) == False:
                self.log("Не удалось поднять картинку")
         #       return False



        return True





def write_message(self , msg = '', trying = 3 ):
    '''
    записываю  текстовое сообщение в окошко фейсбук
    '''
    return controllers.txt_message_write(self, msg)
 
def upload_img(self , img):
   
    kartinka = str(f'{Ini.messages_folder}\\{img}')
    
    controllers.btn_upload_image_click(self)

    selectors = self.fb_ini['locators']['input_image_element_id']

    for selector in selectors:
        inp = self.find(selector , by='id')

        inp.send_keys(kartinka)
        #time.sleep(5)
        #self.driver_implicity_wait(5)
        log_msg = str(f'ЗАГРУЗИЛАСЬ картинка {kartinka}')
        self.log(log_msg)
        return True

    ###################################################

    try:
        pass
        #kartinka = str(f'{Ini.messages_folder}\\{img}')

        #self.find(upload_input_class).send_keys(kartinka)
        ##time.sleep(5)
        ##self.driver_implicity_wait(5)
        #log_msg = str(f'ЗАГРУЗИЛАСЬ картинка {kartinka}')
        #self.log(log_msg)
        #return True
    except Exception :
        log_msg = str(f'Не ЗАГРУЗИЛАСЬ картинка {kartinka}')
        self.log(log_msg)
        return False

def bitul_atraot_mi_daf_FB(self):
    CSS_SELECTOR = '._42ft._4jy0._p._4jy4._517h._51sy'
    self.print(f'''CSS_SELECTOR - {CSS_SELECTOR}''')
    elements =  self.find_elements_by_css_selector_return_elements(CSS_SELECTOR)
    self.print(f"Нашлось {len(elements)} элементов")

    for elem in elements:

        if elem.get_attribute("text") == 'התראות' : 
            self.print(f'elem = {elem.get_attribute("text")}')
            elem.click()
            try: 
                selector_1 = '._4kny._50tm'
                e = self.find_elements_by_css_selector(selector_1)
                e.click()
            except: pass
            try:
                selector_2 = '._7xe-'
                e = self.find_elements_by_css_selector('._7xe-')
                self.log('OTMENIL  --- !')
                e.click()
            except: pass
            time.sleep(2)
            break

