'''@package docstring
Documentation for this module.'''
###############################
#   https://stackoverflow.com/questions/12211781/how-to-maximize-window-in-chrome-using-webdriver-python
###############################
from selenium.webdriver.firefox.options import Options



def chrome_options(self):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--start-maximized")
    options.add_argument("--start-maximized")
    return options

def firefox_options(self):
    options = Options()
    #options.add_argument('--headless')
    options.add_argument("--start-maximized")
    return options
def opera_options(self):
    options = Options()
    #options.add_argument('--headless')
    options.add_argument("--start-maximized")
    return options
def edge_options(self):
    options = Options()
    #options.add_argument('--headless')
    options.add_argument("--start-maximized")
    return options