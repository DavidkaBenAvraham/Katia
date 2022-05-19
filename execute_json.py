from pathlib import Path
import json as json
from logger import Log

from exceptions_handler import ExceptionsHandler as EH


#@Log.log
def loads(path:Path )-> dict :
    ''' получаю объект Path - не str! '''
    with path.absolute().open(encoding='utf-8') as f:
            data = json.loads(f.read())
    return data


def html2json(html:str)->json:
    pass



    



