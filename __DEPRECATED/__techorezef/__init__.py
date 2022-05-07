from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import pandas as pd
import datetime
import time

from Driver import Driver 
from ini_files import Ini
from logger import Log
import execute_json as jsn
import execute_csv as execute_csv
import execute_scenaries as execute_scenaries


import techorezef.product as product
import techorezef.login as login


#class technorezef(Driver):
#    def __init__(self, **kwards): 
#        self.supplier_name = 'techorezef'
#        self.log = Log(self.supplier_name)
#        super().__init__(**kwards)
#        self.self.supplier = jsn.load('techorezef.json')
#        self.scenaries = self.self.supplier["scenaries"]
#        self.supplier_prefics = self.self.supplier["supplier_prefics"]
#        self.supplier_name = self.self.supplier["supplier_name"]
#        self.price_rule = self.self.supplier["price_rule"]
#        self.scenario_files = self.self.supplier["scenaries"]
       
#        #локаторы элементов для сценария логин
#        self.locators['login'] = jsn.load('techorezef_login.json')
#        #локаторы элементов страницы
#        self.locators = jsn.load('techorezef_locators.json')
#        self.json_infinity_scroll = self.self.supplier["infinity_scroll"]
      
#        #Бренды
#        self.brands = jsn.load('brands.json')['brand']
        
#        #Имя текущего файла экспорта CSV
#        self.filename_for_export_data = ''

#        self.ps_list = []
#        pass
  


#    def run(self):
#        self.get_url('https://www.techorezef.co.il/')
#        if login.log_f_in(self): return True
    
#    def fill_df_products_by_scenaries(self , scenario_files ='' ):
#      return execute_scenaries.execute_list_of_scenaries(self , scenario_files)

#    def obrabotaj_polja_tovara(self , p_fields):
#        return product.obrabotaj_polja_tovara(self , p_fields )

def log_in(self):
   
    email = self.locators['login']['email']
    password = self.locators['login']['password']

    open_login_dialog_locator = (self.locators['login']['open_login_dialog_locator']['by'],
                                self.locators['login']['open_login_dialog_locator']['selector'])

    email_locator = (self.locators['login']['email_locator']['by'], 
                        self.locators['login']['email_locator']['selector'])

    password_locator = (self.locators['login']['password_locator']['by'],
                            self.locators['login']['password_locator']['selector'])

    loginbutton_locator =  (self.locators['login']['loginbutton_locator']['by'],
                                self.locators['login']['loginbutton_locator']['selector'])


    open_login_dialog = self.find(open_login_dialog_locator)
    open_login_dialog.click()
    self.find(email_locator).send_keys(email)
    self.find(password_locator).send_keys(password)
    self.find(loginbutton_locator).click()
    self.log('Techorezef logged in')
    return True
