
def login(driver , **login_data):
    driver.get('http://www.facebook.com')

    #driver.find_element_by_id("email").send_keys("one.last.bit@gmail.com")
    #driver.find_element_by_id("pass").send_keys("@o533368048")
    #driver.find_element_by_id("loginbutton").click()

    driver.find_element_by_id("email").send_keys(login_data["email"])
    driver.find_element_by_id("pass").send_keys(login_data["password"])
    driver.find_element_by_id(login_data["loginbutton"]).click()
    return true

