import requests
from dotenv import load_dotenv
import os
import datetime
from pprint import pprint
import argparse
import itertools
import plotly
from plotly import graph_objs as go
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from time import sleep


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Count the number of mentions of search word'
    )
    parser.add_argument(
        'search_key',
        type = str,
        nargs='+',
        help='Search word or phrase'
    )
    parser.add_argument(
        '-p', '--period',
        default=7,
        type=int,
        help='If not specified then considered time period is 7 days',
    )
    parser.add_argument(
        '-m', '--matplotlib',
        type=bool,
        default=False,
        help='Plot statistic data with library Matplotlib'
            ' (and save as png image file) or with Plotly (and get image url)'
    )
    return parser.parse_args()


def get_request_to_vk(method, payload={}, 
        host='https://api.vk.com/method'):
    url = '{host}/{method}'.format(host=host, method=method)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_day_timestamps_from_today(period_in_days=3):
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
        current_date = yesterday - datetime.timedelta(days=timedelta)
        day_before = current_date - datetime.timedelta(days=1)
        day_timestamps.append({
            'date': current_date, 
            'start_timestamp': day_before.timestamp(), 
            'end_timestamp': current_date.timestamp()
        })
    return day_timestamps


class VKWallPostError(Exception):
    pass


def get_stat_for_a_day(payload, vk_method='newsfeed.search'):
    vk_response = get_request_to_vk(vk_method, payload=payload)
    if ('response' not in vk_response.keys() or
            'total_count' not in vk_response['response'].keys()):
        raise VKWallPostError('The answer is missing the required fields'
            '["response"]["total_count"]: \n{}'.format(vk_response))  
    return  vk_response["response"]["total_count"]


def get_stat_for_period(timestamps, access_token, version, search_key,
                        vk_method='newsfeed.search'):
    base_payload = {
        'access_token': access_token,
        'v': version, 
        'q': search_key,
        'count': 1,
    } 
    dates=[]
    counts=[]
    for period in timestamps:
        payload = {
            **base_payload,
            'start_time': period['start_timestamp'],
            'end_time': period['end_timestamp'],
        }
        dates.append(period['date'])
        counts.append(get_stat_for_a_day(payload))
        sleep(0.35)
    return [dates, counts]


def plot_chart_by_matplotlib(stat_data, filepath='chart.png', show_plot=False):   
    fig, ax = plt.subplots()
    ax.plot(stat_data[0], stat_data[1]) 
    ax.format_xdata = mdates.DateFormatter('%d.%m') 
    fig.autofmt_xdate()  
    fig.suptitle('Mentions statistic')
    fig.savefig(filepath)
    if show_plot:
        plt.show()


def plot_chart_by_plotly(stat_data, username, api_key):
    chart_data = [go.Bar(x=stat_data[0], y=stat_data[1])]
    plotly.tools.set_credentials_file(username=username, api_key=api_key)
    image_url = plotly.plotly.plot(chart_data, filename='time-series-simple', auto_open=False)
    return image_url


def main():
    load_dotenv()
    args = parse_arguments()
    access_token = os.getenv("ACCESS_TOKEN")    
    vk_api_version = os.getenv("VERSION") 
    plotly_key = os.getenv("PLOTLY_API_KEY")    
    plotly_username = os.getenv("PLOTLY_LOGIN")       
    stats = list(get_stat_for_period(
                    get_day_timestamps_from_today(args.period),
                    access_token,
                    vk_api_version,
                    ' '.join(args.search_key),
                ))
    if args.matplotlib:
        plot_chart_by_matplotlib(stats)
    else:
        print(plot_chart_by_plotly(stats, plotly_username, plotly_key))

    
if __name__ == '__main__':
    main()
