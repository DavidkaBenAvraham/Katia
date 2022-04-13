from Logging import Log as Log
import DB as db
import datetime
import time
from Ini import Ini

def site_get_all_sku():
    query = str(f'SELECT `supplier_reference`  FROM `gjuj_product` WHERE 1 ')
    pass
