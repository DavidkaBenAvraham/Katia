import bot.config as config
import bot.json as json
from bot import *

def send_all(bot , chat_id):
    print(f''' start sending ''')
    json_messages = json.get_json_from_file('messages.json')
    for json_msg in json_messages:
        print(json_messages[json_msg]['file'])

        #file = json_msg["file"]
        #print(file)
        #bot.send_message(chat_id, str(f'{get_message_from_file(file)}'))
    pass

def get_message_from_file(file):
    print(file)
    with open(file, 'r') as f:
        data = f.read()
    return data
