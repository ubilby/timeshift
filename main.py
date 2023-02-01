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


def show_menu() -> None:
    print(
          '\nEnter command:\n'
          '1. View list of cityes\n'
          '2. Add city\n'
          '3. Exit'
    )


def show_cities(cities: Dict[str, int]):
    current_utc_time: datetime.datetime = (
        datetime.datetime.now(datetime.timezone.utc)
    )
    for city_name in sorted(cities):
        local_time = get_local_time(cities[city_name], current_utc_time)
        print(f'{city_name} - {local_time}')


def find_city() -> Dict[str, str]:
    ABSTRACTAPI_URL: str = (
        'https://timezone.abstractapi.com/v1/current_time?'
        'api_key=6585964da71f44a5aa9b37a5232a1c13&location='
    )
    
    city_name: str = input("Enter city name: ")
    print(city_name)
    city_data: Dict[str, str] = (
        requests.get(ABSTRACTAPI_URL + city_name).json()
    )

    if not city_data:
        print(f'There is not city {city_name}')
        return {}

    return {
        "name": city_name,
        "gmt_offset": city_data["gmt_offset"]
    }


def get_local_time(
    gmt_offset: int,
    base_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
) -> str:

    return (
        base_time + datetime.timedelta(hours=gmt_offset)
    ).strftime('%H:%M')


if __name__ == '__main__':
    cities: Dict[str, int] = dict()

    while True:
        show_menu()
        command: str = input(">>> ")

        if command == '1':
            show_cities(cities)

        elif command == '2':
            city_data = find_city()

            if not city_data:
                continue

            cities[city_data['name']] = int(city_data['gmt_offset'])
            local_time = get_local_time(cities[city_data['name']])
            print(f'Current time in {city_data["name"]} - {local_time}')

        elif command == '3':
            break

        else:
            print(f'Unknown command {command}')
