import Facebook.db as fb_db
import Messages.db as msgs_db
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
def button_send_click(self):
    '''
    кнопка ОТПРАВИТЬ
    ''' 
    btn_send_locator = (self.fb_ini['locators']['btn_send_message']['by'], 
                        self.fb_ini['locators']['btn_send_message']['selector'])
        
    try:
        element = self.find(btn_send_locator).click()
        return True
    except Exception : 
        return False

def btn_start_writting_message_click(self):
        
    '''
    1)  Нажимаю на  'התחל דיון' или 'כתוב פוסט' 
    После нажатия можно начинать записывать сообщение
    '''        
    btn_start_write_message_locator = (self.fb_ini['locators']['btn_start_write_message']['by'], 
                                       self.fb_ini['locators']['btn_start_write_message']['selector'])
        
    elements = self.find(btn_start_write_message_locator)
    if elements  == False: # Не найдена кнопка
        return False

    if str(type(elements)).find("class 'list'") >-1: # vernulos; neskol;ko 
        for elem in elements:
            if elem.text.find('התחל דיון' ) > -1 or elem.text.find('כתוב פוסט') > -1 :
                elem.click()
                return True

    if str(type(elements)).find("webelement") >-1:                
        if elements.text.find('התחל דיון' ) > -1 or elements.text.find('כתוב פוסט') > -1 :
            elements.click()
            return True
def textarea_before_message_focus(self):
    #textarea_navigationFocus_locator = (self.fb_ini['locators']['textarea_navigationFocus']['by'],
    #                                        self.fb_ini['locators']['textarea_navigationFocus']['selector'])
    #textarea_navigationFocus = self.find(textarea_navigationFocus_locator)
    #textarea_navigationFocus.click()
    script = str(f'''document.getElementsByClassName('{self.fb_ini['locators']['textarea_navigationFocus']['selector']}').innerHTML = "текст"''')
    self.log(script)
    self.driver.execute_script(script)
    pass
def txt_message_write(self, msg):
    #msg = msg.encode('utf-8')
    input_text_message_locator = (self.fb_ini['locators']['input_text_message']['by'],
                                  self.fb_ini['locators']['input_text_message']['selector'])
   
    self.wait(5)
    element = self.find(input_text_message_locator)
    self.log(str(f'''
    ###############  Результат. \n
    Селектор {input_text_message_locator}   элемент {element} '''))
    if element != False:
        #после дебага вставить в блок try
        #self.driver.execute_script("arguments[0].click();", element)
        #self.driver.execute_script(f"arguments[0].insertAdjacentText('afterbegin','{str(msg)}');", element)
        element.click()
        element.send_keys(msg)
        self.log(f'Сообщение записано ')
        return True

        try: # @Попал
            #script = str(f'''document.getElementsByClassName('{CSS_JS_SELECTOR}').innerHTML = 'текст'''')
            #self.log(script)
            #self.driver.execute_script(script)
            ##element.send_keys(msg)
            #self.log(f'Сообщение записано ')
            #return True
            
            pass
        except ElementNotInteractableException as e:
            self.log(f'''{CSS_SELECTOR} не найден селектор для ввода сообщения! 
            Не нашлось поле ввода для сообщения! {e}''')
            return False

def btn_upload_image_click(self):
    btn_upload_image_locator = (self.fb_ini['locators']['btn_upload_image']['by'], 
                                self.fb_ini['locators']['btn_upload_image']['selector'])
    elements = self.find(btn_upload_image_locator)
    try:
        if str(type(elements)).find("class 'list'") >-1:
            for elem in elements:
                if elem.text.find('תמונה/סרטון') > -1  :
                    elem.click()
                    break
                    return True

        if str(type(elements)).find("webelement") >-1:                      
            if elements.text.find('תמונה/סרטון') > -1  :
                elements.click()
                return True

    except StaleElementReferenceException as ex: #
        self.log(ex)

