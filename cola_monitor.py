import requests
from dotenv import load_dotenv
import os
import datetime
from pprint import pprint


SECONDS_IN_DAY = 24*60*60



def get_request_to_vk(method, payload={}, 
        host='https://api.vk.com/method'):
    url = '{host}/{method}'.format(host=host, method=method)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_day_timestamps_from_today(period_in_days=7):
    now_date = datetime.date.today()
    yesterday = datetime.datetime(
        year=now_date.year, 
        month=now_date.month,
        day=now_date.day,
        hour=0,
        tzinfo=datetime.timezone.utc,
    )
    day_timestamps = []
    for timedelta in range(1, period_in_days+1):
        day_timestamps.append({
            'date': (yesterday - datetime.timedelta(days=timedelta)), 
            'start_timestamp': (yesterday - datetime.timedelta(days=(timedelta+1))).timestamp(), 
            'end_timestamp': (yesterday - datetime.timedelta(days=timedelta)).timestamp()
        })
    return day_timestamps


def main():
    load_dotenv()
    service_key = os.getenv("SERVICE_KEY")
    access_token = os.getenv("ACCESS_TOKEN")    
    vk_api_version = os.getenv("VERSION")
    base_payload = {
        'access_token': access_token,
        'v': vk_api_version,  
    }
    pprint(get_day_timestamps_from_today())
    exit()    
    current_date = datetime.datetime.today()
    yesterday = current_date - datetime.timedelta(days=1)
    yesterday_midnight = datetime.datetime(
        year=yesterday.year, 
        month=yesterday.month,
        day=yesterday.day,
        hour=0,
        tzinfo=datetime.timezone.utc,
    )
    end_time = int(yesterday_midnight.timestamp())
    start_time = end_time - SECONDS_IN_DAY
    payload = {
        **base_payload,
        'q': 'coca-cola',
        'count': 1,
        'start_time': start_time,
        'end_time': end_time,
    }
    print(payload)
    response = get_request_to_vk('newsfeed.search', payload=payload)
    print(response)
    print(response['response']['total_count'])



if __name__ == '__main__':
    main()



#newsfeed.search