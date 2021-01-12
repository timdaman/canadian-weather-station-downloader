"""
This is a small program that downlands data about all of the currently active
weather stations in Canada and exports that in CSV format.

The goal of this is to produce a CSV suitable to use with Google "My Maps".

What is my goal? I use weather data to determine if the ice on small lakes in
an area is likely safe to travel on. To do this I process the data of a
weather station hour by hour and imagine a lake is right next to them.

I do not want to use forecast data from the area I am going as that is
synthesized and may have various biases. What i use the data from the nearest
weather station. This program helps im mapping all of the weather active
stations and then visually I can determine which one most best for my
destination.

This program is slow. This is kind to the Weather API and given I plan to
run it once a year that is not a issue.
"""
from typing import Iterable

"""
Copyright 2021 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from collections import OrderedDict
from csv import DictWriter
from datetime import date, timedelta

import bs4
import requests

today = date.today()
# The APIs do not present today until the day is complete. As a result we look for stations with data yesterday
yesterday = today - timedelta(days=1)
y_year = yesterday.year
y_month = yesterday.month
y_day = yesterday.day

host = 'https://climate.weather.gc.ca'


def generate_stations(api_host: str = host, year: int = y_year, month: int = y_month, day: int = y_day) \
        -> Iterable[int]:
    """Returns every ective station ID one at time"""

    start = 0
    interval = 100
    while True:
        station_list_url = f'{api_host}/historical_data/search_historic_data_stations_e.html?' \
                           f'searchType=stnProv&' \
                           f'timeframe=1' \
                           f'&lstProvince=' \
                           f'&StartYear=1840' \
                           f'&EndYear={year}' \
                           f'&optLimit=specDate' \
                           f'&Year={year}' \
                           f'&Month={month}' \
                           f'&Day={day}' \
                           f'&selRowPerPage={interval}' \
                           f'&startRow={start}'
        print(f"Starting at {start} ", end='', flush=True)
        response = requests.get(station_list_url, allow_redirects=True)
        assert response.status_code == 200
        assert b'Sorry' not in response.content
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        base = soup.find(class_='historical-data-results')
        if base is None:
            print("All stations processed!")
            break

        station_list = base.find_all("form")

        for station in station_list:
            station_id = station.find("input", attrs={'name': "StationID"})['value']
            province = station.find("input", attrs={'name': "Prov"})['value']
            print(".", end='', flush=True)
            yield station_id
        print("")
        start += interval


def get_station_details(station_id: int, api_host: str = host, year: int = y_year, month: int = y_month,
                        day: int = y_day):
    """Give, a station ID return the meta data."""
    details = OrderedDict()

    details['StationID'] = station_id
    details['url'] = f"{api_host}/climate_data/daily_data_e.html?" \
                     f"&StationID={station_id}" \
                     f"&Prov=" \
                     f"&urlExtension=_e.html" \
                     f"&searchType=stnProv&optLimit=specDate" \
                     f"&StartYear=1840" \
                     f"&EndYear={year}" \
                     f"&selRowPerPage=100" \
                     f"&Line=2" \
                     f"&Month={month}" \
                     f"&Day={day}" \
                     f"&lstProvince=" \
                     f"&timeframe=2" \
                     f"&Year={year}"

    response = requests.get(details['url'])
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    title_block = soup.select_one("p.table-header").contents
    details['name'] = title_block[0]
    details['province'] = title_block[2]

    for field in ['latitude', 'longitude', 'elevation', 'climateid', 'wmoid', 'tcid']:
        details[field] = soup.select_one(f'div[aria-labelledby={field}]').text.lstrip(' ')
    return details


def main():
    filename = f"canada_weather_station_data_{y_year}-{y_month}-{y_day}.csv"
    print(f'Writting {filename}')
    with open(filename, 'w', newline='') as csvfile:
        first = True
        writer = None
        for station_id in generate_stations():
            details = get_station_details(station_id=station_id)
            if first:
                writer = DictWriter(csvfile, fieldnames=details.keys())
                writer.writeheader()
                first = False
            writer.writerow(details)

if __name__ == '__main__':
    main()
