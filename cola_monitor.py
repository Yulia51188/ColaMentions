import requests
from dotenv import load_dotenv
import os
import datetime


SECONDS_IN_DAY = 24*60*60



def get_request_to_vk(method, payload={}, 
        host='https://api.vk.com/method'):
    url = '{host}/{method}'.format(host=host, method=method)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    service_key = os.getenv("SERVICE_KEY")
    access_token = os.getenv("ACCESS_TOKEN")    
    vk_api_version = os.getenv("VERSION")
    base_payload = {
        'access_token': access_token,
        'v': vk_api_version,  
    }
    
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