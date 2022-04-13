import DB as db
import time 

def read_all():
    guery = "select * from bot_advertising"
    return db.execute(guery)
    

def start_sender(update , pause:float):
    while True:
        msgs = read_all()
        for index , row in msgs.iterrows():
            update.message.reply_text(row['adv'])
            time.sleep(pause)
        pass

def add_adv(adv: str) -> None:
    guery = "insert into  bot_advertising (adv) values ('{adv}')"
    return db.execute(guery , do='insert')
    pass

def get_adv_from_db() ->[]:
    msgs = []
    msgs_in_db = read_all()
    for index , row in msgs_in_db.iterrows():
        msgs.append(row['adv'])
    return msgs
