from Logging import Log as Log
import DB as db
import datetime
import time
from Ini import Ini

def log_status_sent_message_2fbgroup(self , msg_id, grp_id, status):
    '''
    логгирование отправленных сообщений
    '''
    query = str(f'''insert into logging (msg_id, grp_id, status) values ({msg_id}, {grp_id}, {status})
    ''')
    return db.execute(query , do = 'insert')

def get_one_message(self , msg_id):
    query = str(f'''select ROWID , 
    lang,
    sug,
    tiur_katzar,
    message,
    mehir,
    message_folder, 
    message_file_name, 
    message_images_names 
    from messages  where ROWID = {msg_id}
    ''' )
    return db.execute(query)

    pass
def get_messages(lang = '*' , 
                 sug = '*' , 
                 message_status = 'active' , 
                 ROWID = '*',  
                 return_as_dataframe = True) :
    '''
    lefarsem_bekvutza : В КАКОЙ ТИП ГРУППЫ РЕКЛАМИРОВАТЬ
    '''
    query = str(f'''select ROWID , 
    lang,
    sug,
    tiur_katzar,
    message,
    mehir,
    message_folder, 
    message_file_name, 
    message_images_names 
    from messages  
    ''' )
    required_and = False

    if ROWID != "*": 
        query += str(f' where  ROWID = {ROWID}')
        required_and = True

    if lang != "*": 
        if required_and:
             query += ' and '
        else :   
            query += ' where ' 
        query += str(f'  lang = "{lang}"')
        required_and = True

    if sug != "*": 
        if required_and:
             query += ' and '
        else :   
            query += ' where ' 
        query += str(f'  sug = "{sug}"')
        required_and = True


    if message_status != "*": 
        if required_and:
             query += ' and '
        else :   
            query += ' where ' 
        query += str(f'  message_status = "{message_status}"')
        required_and = True
    log = Log()
    log.write(query)
    return db.execute(query = query , return_as_dataframe = return_as_dataframe)

def add_new_message(lang,sug,tiur_katzar,message,mehir,message_folder,message_file_name,message_images_names):
    dt = Ini.get_now()
    query = str(f'''insert into messages (
    lang,
    sug,
    creaion_date,
    tiur_katzar,
    message,
	mehir,
    message_folder,
    message_file_name,
    message_images_names , 
    message_status) 
    values(
    "{lang}",
    "{sug}",
    "{dt}",
    "{tiur_katzar}",
    "{message}",
    "{mehir}",
    "{message_folder}",
    "{message_file_name}",
    "{message_images_names}" , 
    "active")''')


    return db.execute(query = query , do = 'insert')
    pass

