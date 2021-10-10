from sys import argv
from datetime import datetime
import psycopg
import requests
import config

### Insert measurement to database, retrieve data needed for further calculations
added = int(argv[1])
time_now_datetime = datetime.now()
time_now_string = time_now_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')

with psycopg.connect(f'dbname={config.db_name} user={config.db_user} password={config.db_pass} host={config.db_host}') as conn:
    with conn.cursor() as cur:
        cur.execute(f'''
        INSERT INTO tray_table (add_time, added)
        VALUES ('{time_now_string}', {added})
        ''')

requests.get(f'{config.domoticz_url}/json.htm?type=command&param=switchlight&idx={config.domoticz_add_switch_idx}&switchcmd=Set%20Level&level=0')
