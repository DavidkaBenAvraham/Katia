
def logged_in(self):
   
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

