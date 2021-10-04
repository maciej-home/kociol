from sys import argv
from datetime import datetime, timedelta
import requests
import psycopg
import config

### Insert measurement to database, retrieve data needed for further calculations

measurement = int(argv[1])
time_now_datetime = datetime.now()
time_now_string = time_now_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
time_24h_before_now = (time_now_datetime - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S.%f')
current_month_first_day = time_now_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
previous_month_last_day = current_month_first_day - timedelta(microseconds=1)
previous_month_first_day = previous_month_last_day.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

with psycopg.connect(f'dbname={config.db_name} user={config.db_user} password={config.db_pass} host={config.db_host}') as conn:
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

        cur.execute(f'''SELECT measurement FROM test_table WHERE measurement_time >= '{previous_month_first_day}'
        ORDER BY measurement_time, measurement_id, measurement LIMIT 1''')
        previous_month_start_impulses = cur.fetchone()[0]

        cur.execute(f'''SELECT measurement FROM test_table WHERE measurement_time <= '{previous_month_last_day}'
        ORDER BY measurement_time DESC, measurement_id DESC, measurement DESC LIMIT 1''')
        previous_month_end_impulses = cur.fetchone()[0]

### Calculate used fuel etc. and send to domoticz

season_impulses = measurement - season_start_impulses
coal_season = season_impulses * config.ratio
last24h_impulses = measurement - last_24h_start_impulses
coal_last24h = last24h_impulses * config.ratio
previous_month_impulses = previous_month_end_impulses - previous_month_start_impulses
coal_previous_month = previous_month_impulses * config.ratio

if config.domoticz_enabled:
    requests.get(f'{config.domoticz_url}/json.htm?type=command&param=udevice&idx={config.domoticz_season_idx}&nvalue=0&svalue={round(coal_season, 1)}')
    requests.get(f'{config.domoticz_url}/json.htm?type=command&param=udevice&idx={config.domoticz_last24h_idx}&nvalue=0&svalue={round(coal_last24h, 1)}')
    requests.get(f'{config.domoticz_url}/json.htm?type=command&param=udevice&idx={config.domoticz_previous_month_idx}&nvalue=0&svalue={round(coal_previous_month, 1)}')