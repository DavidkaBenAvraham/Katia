
from selenium.common.exceptions import *
import DB as db
import datetime
import time
from Ini import Ini

#from Logging import Log as Log


class SeleniumException:
    '''
        NoSuchElementException,
        NoSuchWindowException,
        NoSuchFrameException,
        NoAlertPresentException,
        InvalidSelectorException,
        ElementNotVisibleException,
        ElementNotSelectableException,
        TimeoutException,
        StaleElementReferenceException
    '''
    def __init__(self , **kwards):
        #self.log(kwards)
        pass

class IoExsception:
    try: pass
    except IOError:
        self.log('An error occurred trying to read the file.')

    except ValueError:
        self.log('Non-numeric data found in the file.')

    except ImportError:
        self.log("NO module found")

    except EOFError:
        self.log('Why did you do an EOF on me?')

    except KeyboardInterrupt:
        self.log('You cancelled the operation.')

    except:
        self.log('An error occurred.')

class Sqlite3Exception:
    pass
# def cath(E) -> Exception :
def cath(E = '' , 

            lang = '',
            msg_id='',
            grp_id='',

            err_msg = '' , 
            log_msg = '' , 
            prog_module = '',

         ):  
    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = str(f'''insert into logging (
    date ,     
    
    lang,
    msg_id,
    grp_id,

    prog_module,  
    err_msg, 
    log_msg , 
    err  
    ) 

    values
    
    (    
    "{Ini.dt_get_now()}" , 

    "{lang}" ,
    "{msg_id}" ,
    "{grp_id}" ,

    "{prog_module}" , 
    "{err_msg}" , 
    "{log_msg}" , 
    "{str(E)}"
    )''')
    db.execute(query=query , do='insert')
    return False

def cath_connector_Error(E , err_msg = ''):
    '''
    исключения коннектора БД
    '''
    if E.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
            self.log("Something is wrong with your user name or password")
    elif E.errno == errorcode.ER_BAD_DV_ERROR:
        self.log("Database does not exist")
    else:
        self.log(E)
