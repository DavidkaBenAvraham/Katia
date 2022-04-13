
def logged_in(self):


    open_login_dialog_locator = (self.locators['login']['open_login_dialog_locator']['by'],
                                  self.locators['login']['open_login_dialog_locator']['selector'])


    email = self.locators['login']['email']
    password = self.locators['login']['password']

    email_locator = (self.locators['login']['email_locator']['by'], 
                        self.locators['login']['email_locator']['selector'])

    password_locator = (self.locators['login']['password_locator']['by'],
                            self.locators['login']['password_locator']['selector'])

    loginbutton_locator =  (self.locators['login']['loginbutton_locator']['by'],
                                self.locators['login']['loginbutton_locator']['selector'])



    self.find(open_login_dialog_locator).click()
   
    self.find(email_locator).send_keys(email)
    self.find(password_locator).send_keys(password)
    loginbutton = self.find(loginbutton_locator)
    loginbutton[1].click()
    #self.log(loginbutton)
    #self.log('DORNET logged in')
    return True

