'''
Application of viewing locacl times of cityes

There are threee puncts menu:
    view list of cityes
    add city
    exit

There is findig city by service abstracpapi.com
If city will be find name of city will be save to local storage of the app
'''
import datetime
from typing import Dict
import requests

ABSTRACTAPI_URL: str = (
    'https://timezone.abstractapi.com/v1/current_time?'
    'api_key=6585964da71f44a5aa9b37a5232a1c13&location='
)
cities: Dict[str, int] = dict()

while True:
    print(
        '\nEnter command:\n'
        '1. View list of cityes\n'
        '2. Add city\n'
        '3. Exit'
    )
    command: str = input(">>> ")

    if command == '1':

        for city_name in cities:
            local_time = (
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(hours=cities[city_name])
            ).strftime('%H:%M')
            print(f'{city_name} - {local_time}')

    elif command == '2':
        city_name: str = input("Enter city name: ")
        print(city_name)
        city_data: Dict[str, str] = (
            requests.get(ABSTRACTAPI_URL + city_name).json()
        )

        if not city_data:
            print(f'There is not city {city_name}')

        else:
            local_time = (
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(hours=int(city_data['gmt_offset']))
            ).strftime('%H:%M')
            print(f'Current time in {city_name} - {local_time}')
            cities[city_name] = int(city_data['gmt_offset'])

    elif command == '3':
        break

    else:
        print(f'Unknown command {command}')
