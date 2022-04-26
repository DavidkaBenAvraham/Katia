from pathlib import Path
import json


def loads(path:Path)->json:
    ''' получаю объект Path - не str! '''
    with path.open(encoding='utf-8') as f:
            data = json.loads(f.read())
    return data
