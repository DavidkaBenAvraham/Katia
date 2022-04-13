import json
import bot.config as config


def get(file):
    path = f'''{config.path}\\{file}''' 
    print(path)
    with open(path, 'r') as f:
        data = json.loads(f.read())
    return data

