########################################################################
#    
#                                                                     
#               класс FB все, что касается фейсбука
#               от него наследуют классы:
#                   Sender
#                   Ini
#
#
#               fb запускает браузер и выставил ожидание перед 
#               каждым действием драйвера
#
########################################################################  

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

import pandas as pd
import datetime
import time
import sys

import Facebook.db as fb_db
import Messages.db as msgs_db

import Facebook.scenario.login as login_scenario
import Facebook.scenario.message as message
import Facebook.scenario.message_controllers as controllers

from Driver import Driver 
from ini_files_dir import Ini
import execute_json as json
from logger import Log


from PyQt5 import QtWidgets
from Facebook.ui.QT_login_controller import qt_login as qt_login
from Messages.ui.QT_messages_editor_controller import qt_messages_window
from Messages.ui.QT_messages_editor_controller import PandasModel

import sys

class FB(Driver):
    '''
    Методы класса:
    run() : Запуск класса и логин на фб
    start_sender(self , sug = '*', lang = '*', from_ROWID = 0 , to_ROWID = 'max'): старт рассылки сообщений
    '''

    def __init__(self, **kwards): 
        super().__init__(**kwards)
        self.fb_ini = json.load('facebook.json')
        self.log('запустился класс FB')
        self.controllers = controllers


        #------------------------
        self.un = '' # username
        self.passwrd = '' # password
        #------------------------
        self.current_message = '' # сообщение для рекламы с которым сейчас идет работаю


    def ui_login_window(self):
        app = QtWidgets.QApplication([])
        self.login_window = qt_login(self)
        self.login_window.show()
        self.login_window.set_username_password(email , password)
        self.log("START GUI ")
        sys.exit(app.exec_())

    def ui_messages_Table(self):
        app = QtWidgets.QApplication([])
        self.qt_messages_window = qt_messages_window(self)
        self.qt_messages_window.show()
        sys.exit(app.exec_())
        pass


    def run(self  , gui = False):
        self.get_url("https://facebook.com")
        
        if gui: return self.ui_login_window() # отрываю лончер(un, passwrd) если надо 
        else: return self.login()
        
        
    def login(self):
        return login_scenario.run(self)


    def check_login(self):
        return login_scenario.check_login(self) 
    

    def send(self , sug = '*', lang = '*', from_ROWID = 0 , to_ROWID = 'max' ):

        '''
        Старт рассылок

        sug_kvutza = тип группы в фейсбук
        От него зависит в какое поле я ввожу и какие данные
        это может быть קבוצת פירסום
        או
        קבוצת מחירות
        '''
        self.check_login()

        '''
        первое дробление потока рассылок
        идет по языку. В зависимости от языка группы я 
        отсылаю ртелевантные мессаджи к языку
        '''
        if lang == "*": 
            langs = ['he','ru']
        else: langs = lang
        
        for lang in langs: 
            self.set_current_lang(lang) # глобально устанавливаю язык на котором буду делать отправку
            self.log(str(f'Старт рассылок для языка {self.get_current_lang()}'))

            self.messages_bundle = msgs_db.get_messages(lang = lang , sug = sug )
            '''
            из таблицы сообщений 
            сохраняю датафрейм сообщений для групп на этом языке
            '''
            
            if not type(self.messages_bundle) is pd.DataFrame  :   
                self.log('''
                не удалось получить сообщения для рассылки 
                ''')
                return False


            for  index, row  in self.messages_bundle.iterrows() :
                '''
                беру по одному сообщению из dataFrame и отсылаю в группы
                '''
                self.set_current_message(row)
                self.log(str(f'''Старт рассылки сообщения  
                ************************************************
                msg (self.get_current_message_id()) = {self.get_current_message_id()}
                txt (self.get_current_message_text()) = {self.get_current_message_text()}
                lang (self.get_current_lang()) =  {self.get_current_lang()}
                
                ************************************************
                '''))

                if message.send_single_message_into_many_groups(self , 
                                                msg_id = self.get_current_message_id(), 
                                                sug = sug , 
                                                from_ROWID = from_ROWID, 
                                                to_ROWID = to_ROWID):
                    '''
                    Отсюда отправляется сообщение msg = self.get_current_message_text() 
                    в группы
                    '''
                    self.log(str(f'Сообщение  послано. Пауза {60 * 15} сек'))
                    time.sleep(60 * 15)


    def send_single_message_into_one_group(self, fbgroup_id, msg_id):
        '''
        Используются для дебаггинга
        '''
        message.send_single_message_into_one_group(self , msg_id, fbgroup_id)
        pass



    '''
    устанавливаю мессадж с  которым работаю в данное время в глобальную достунпность.
    потом я смогу его дергать по частям функциями 
    get_current_message()
    get_current_message_id()
    get_current_message_text()
    '''
    def set_current_message(self , current_message):
        self.current_message = current_message

    '''
    Для удобства обработки сообщения я создал функции
    возвращающие текст и идентификатор сообщения
    '''
    def get_current_message(self):
        try:
            return self.current_message
        except: return False
    def get_current_message_id(self):
        try:
            return self.current_message["ROWID"]
        except: return -1
    def get_current_message_text(self):
        try:
            return self.current_message["message"]
        except: return -1
    def get_current_message_images(self):
        try:
            return self.current_message["message_images_names"]
        except: return -1



    '''
    Как и с мессаджами мне удобней работать с группой из глобальной доступности
    потом я смогу его дергать по частям функциями 
    get_current_facebookgroup()
    get_current_facebookfbgroup_id()
    '''
    def set_current_facebookgroup(self , current_facebookgroup):
        self.current_facebookgroup = current_facebookgroup

    def get_current_facebookgroup(self):
        try:
            return self.current_facebookgroup
        except: return -1

    def get_current_facebookfbgroup_id(self):
        try:
            return self.current_facebookgroup["ROWID"]
        except: return -1

    def set_current_lang(self, current_lang):
        self.current_lang = current_lang


    def get_current_lang(self):
        try: return self.current_lang
        except: return '*'

