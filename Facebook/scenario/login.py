from logger import Log
 
import Facebook.db as db
from ini_files import Ini


def run(self):
    self.log("LOGIN")
    email_locator = (self.fb_ini['login']['email_selector']['by'],
                     self.fb_ini['login']['email_selector']['selector'])

    password_locator = (self.fb_ini['login']['password_locator']['by'],
                        self.fb_ini['login']['password_locator']['selector'])

    loginbutton_locator = (self.fb_ini['login']['loginbutton_locator']['by'],
                           self.fb_ini['login']['loginbutton_locator']['selector'])

    self.find(email_locator).send_keys(self.fb_ini['login']['email'])
    self.find(password_locator).send_keys(self.fb_ini['login']['password'])
    self.find(loginbutton_locator).click()
    self.log("Успешный логин на фейсбук")
    self.fb_login = True
    return True
    try:
            pass
    except Exception : 
        self.log(str(f''' Не залогинился на фейсбук  '''))
        self.login = False
        return False

def check_login(self):
    if  self.fb_login == False : return run(self)
    self.log("проверка логин")
    '''
    если есть поле ввода email 
    значит надо пройти логин
    '''
    email_locator = (self.fb_ini['login']['email_selector']['by'],
                     self.fb_ini['login']['email_selector']['selector'])
    try:
        email = self.find(email_locator)
        if email != False: return run(self)
        else: 
            self.log("Порверка логина пoдтверждена отсутствием поля email")
            return True
    except: return True


