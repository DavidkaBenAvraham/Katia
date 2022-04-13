from Logging import Log as Log
import DB as db
import datetime
import time
from Ini import Ini


'''
select * from fbgroups where ROWID NOT IN (
SELECT grp_id FROM `logging` WHERE status =0 and msg_id = {msg_id}
)
'''

def get_languages():
    pass

def insert_into_facebook_groups_types(**kwards):
    '''
    for key in kwards:
        key (ключ): kwards.key (значение)
    '''
    pass

def update_url(ROWID , **kwards):
    query = str(f'update fbgroups set ')
    i=1
    for key in kwards:
        query += str(f'{key} = "{kwards.key} "')
        if len(kwards) > 1 and i < len(kwards): 
            query += " and "
            i += 1
    
    query += str(f' where ROWID = {ROWID}')

    db.execute(query = query , do = 'update')

def insert_fbgroups(data):
    ''' из disct_sql_values
    получаю словарь данных для вставку в таблицу
    групп для  рассылок
    '''
    query = 'insert into fbgroups ("url","group_title","sug_kvutza","lang") values '

    for d in data:
         query += str(f'("{d[0]}","{d[1]}","{d[2]}","{d[3]}")')
    return db.execute(query)
    pass

def get_fbgroups(lang='ru', msg_id = -1,
               sug_kvutza='*', 
               status_kvutza = 'active' , 
               order_by = '',
               from_ROWID = 0, to_ROWID = 'max',
               return_as_dataframe = True):
    '''
    если msg_id =  -1 сообщение пересылается во все группы
    если есть msg_id - проверяю по логу, куда сообщение уже
    было отправлено и игнорирую их
    status_kvutza: active;paused;down;*
    sug_kvutza: 1;2;3;*

    по умолчанию возвращает датафрейм
    '''


    query = str(f'''select ROWID, url, lang, sug_kvutza,   group_title , status_kvutza, pirsum_axaron, 
    zman_pirsum_axaron, status_pirsum_aharon  from fbgroups ''')
    
    required_and = False # добавлать and в условия
    
    query += str(f''' where ROWID > {from_ROWID} ''')
    if to_ROWID != 'max': query += str(f' and  ROWID < "{ROWID}" ')
    if sug_kvutza != '*': query += str(f' and  sug_kvutza = "{sug_kvutza}" ')
    if lang != '*': query += str(f' and  lang = "{lang}" ')
    if status_kvutza != "*": query += str(f' and status_kvutza = "{status_kvutza}" ')

    if msg_id >0 : query += str(f'''and  ROWID NOT IN (
            SELECT grp_id FROM `logging` WHERE status = 1 and msg_id = {msg_id}
        )  ''')

    if order_by != '': query += str(f' and order by = "{order_by}" ')

    return db.execute(query,  return_as_dataframe = return_as_dataframe)
    pass


def get_fbgroup_url(self , fbgroup_id):
    query = str(f'''select url from fbgroups where ROWID = {fbgroup_id} ''')
    fbgroup_url = db.execute(query , return_as_dataframe = False)
    fbgroup_url = fbgroup_url[0]
    fbgroup_url = str(fbgroup_url).replace("',)" ,"")
    fbgroup_url = str(fbgroup_url).replace("('" ,"")
    
    return fbgroup_url

def get_fbgroup(self , fbgroup_id):
    '''
    получаю данные одной группы по ее ROWID
    '''
    query = str(f'''select ROWID, url, lang, sug_kvutza,   group_title , status_kvutza, pirsum_axaron, 
    zman_pirsum_axaron, status_pirsum_aharon  from fbgroups where ROWID = {fbgroup_id} ''')

    return db.execute(query , return_as_dataframe = False)
    pass

def write_message_status(ROWID , status_pirsum_aharon):
    query = str(f'update fbgroups set status = "{status_pirsum_aharon}" where ROWID = {ROWID}') 
    return db.execute(query = query)
    pass


