from pathlib import Path
import json as json
from logger import Log

from exceptions_handler import ExceptionsHandler as EH

#@print
def loads(path:Path )-> dict :
    ''' получаю объект Path - не str! '''
    with path.absolute().open(encoding='utf-8') as f:
            data = json.loads(f.read())
    return data

def dump(data , path:Path):
    if str(type(data)).find('list')>-1: 
        data = json.dumps(data).replace('[','{').replace(']','}')
    with path.absolute().open('w',encoding='utf-8') as f:
            json.dump(data ,f)

def html2json(html:str)->json:
    pass



    



