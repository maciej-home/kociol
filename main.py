from sys import argv
from datetime import datetime, timedelta
import psycopg
import config

### Insert measurement to database, retrieve data needed for further calculations

measurement = int(argv[1])
time_now_datetime = datetime.now()
time_now_string = time_now_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
time_24h_before_now = (time_now_datetime - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S.%f')

with psycopg.connect('dbname=test user=test_user password=test host=localhost') as conn:
    with conn.cursor() as cur:
        cur.execute(f'''
        INSERT INTO test_table (measurement_time, measurement)
        VALUES ('{time_now_string}', {measurement})
        ''')

        cur.execute(f'''SELECT measurement FROM test_table WHERE measurement_time >= '{config.season_start}'  
        ORDER BY measurement_time, measurement_id, measurement LIMIT 1''')
        season_start_impulses = cur.fetchone()[0]

        cur.execute(f'''SELECT measurement FROM test_table WHERE measurement_time >= '{time_24h_before_now}'  
        ORDER BY measurement_time, measurement_id, measurement LIMIT 1''')
        last_24h_start_impulses = cur.fetchone()[0]

### Calculate used fuel etc. and send to domoticz

season_impulses = measurement - season_start_impulses
coal_season = season_impulses * config.ratio
last24h_impulses = measurement - last_24h_start_impulses
coal_last24h = last24h_impulses * config.ratio
