"""
Application of viewing locacl times of cityes

There are threee puncts menu:
    view list of cityes
    add city
    exit

There is findig city by service abstracpapi.com
If city will be find name of city will be save to local storage of the app
"""
import datetime
from sys import exit
from typing import Dict, Callable
import requests


class CityDataFetcher:
    def fetch_city_data(self, city_name: str):
        raise NotImplementedError("There is not realisation!")


class City:
    def __init__(self, name: str, timezone: int):
        self.timezone: int = timezone
        self.name: str = name


class Application:
    def __init__(self, fetcher: CityDataFetcher):
        self.fetcher = fetcher
        self.cities: Dict[str, City] = dict()
        self.commands: Dict[str, Callable] = {
            '1': self.show_cities_list,
            '2': self.add_city,
            '3': self.exit
        }

    def show_menu(self) -> None:
        print(
            "\nEnter command:\n"
            "1. View list of cityes\n"
            "2. Add city\n"
            "3. Exit"
        )

    def handle_user_input(self):
        command = input('>>> ')

        if command in self.commands:
            self.commands[command]()

        else:
            print(f"Unknown command {command}")

    def show_cities_list(self) -> None:
        current_utc_time: datetime.datetime = (
            datetime.datetime.now(datetime.timezone.utc)
        )
        for city_name in sorted(self.cities):
            local_time = get_local_time(
                self.cities[city_name].timezone,
                current_utc_time
            )
            print(f"{city_name} - {local_time}")

    def add_city(self) -> None:
        city_name: str = input("Enter city name: ")
        city_data = self.fetcher.fetch_city_data(city_name)

        if not city_data:
            print(f"There is not city {city_name}")

        city = City(city_name, city_data["gmt_offset"])
        self.cities[city_name] = city
        print(city_name, get_local_time(city.timezone), sep=' - ')

    def exit(self):
        exit(0)


class AbstractAPI(CityDataFetcher):
    ABSTRACTAPI_URL: str = (
        "https://timezone.abstractapi.com/v1/current_time?"
        "api_key=6585964da71f44a5aa9b37a5232a1c13&location="
    )

    def fetch_city_data(self, city_name) -> Dict[str, str]:
        city_data: Dict[str, str] = (
            requests.get(self.ABSTRACTAPI_URL + city_name).json()
        )

        if not city_data or city_data.get('error', False):
            return {
                'error': f'Town {city_name} don`t found'
            }

        return {
            'gmt_offset': city_data['gmt_offset'],
            'name': city_name
        }


def get_local_time(
    gmt_offset: int,
    base_time: datetime.datetime = (
        datetime.datetime.now(datetime.timezone.utc)
    )
) -> str:

    return (base_time + datetime.timedelta(hours=gmt_offset)).strftime("%H:%M")


if __name__ == "__main__":
    fetcher = AbstractAPI()
    app = Application(fetcher)

    while True:
        app.show_menu()
        app.handle_user_input()
