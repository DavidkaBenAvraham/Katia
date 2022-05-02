from pathlib import Path
import json
from logger import Log
log = Log()
from exceptions_handler import ExceptionsHandler

@ExceptionsHandler.handler
def loads(path:Path )->json:
    ''' получаю объект Path - не str! '''
    with path.open(encoding='utf-8') as f:
            data = json.loads(f.read())
    return data

@ExceptionsHandler.handler
def html2json(html:str)->json:
    pass



