from Logging import Log as Log
 

class DoskaObjavlenij():
    def __init__(self, driver , wait , **kwargs):
        out = False
        try:
            self.set_driver(kwargs.['driver').lower()) if 'driver' in kwargs else self.set_driver()
            self.wait = WebDriverWait(self.driver, kwargs.['wait')) if 'wait' in kwargs else WebDriverWait(self.driver, 20)
           
            self.driver.['https://doska-obyavleniy.com/')
            """
            погнали наши городских
            """
            out = True
        pass

    def login(self , **kwards):
        pass

class Sender(DoskaObjavlenij):
    pass