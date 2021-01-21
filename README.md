This is a utility to download the current list of active weather stations in Canada.

Currently, this downloads information about the Environment Canada weather
stations and produces a CSV file with their details including
* Lat and Long
* Various IDs used to identify the station
* The station name
* A link to the historical records for this station

I wrote this utility to produce CSV files for use with Google's "My Maps" 
feature.

## Installation and use
    # This assumes you have Python and pipenv installed
    git clone https://github.com/timdaman/canadian-weather-station-downloader.git
    cd canadian-weather-station-downloader
    pipenv install
    pipenv run ./download_stations.py

## Why would I need a map of weather stations in Canada? 
I do lots of wilderness travel. I sometimes like to analyze recent weather data
for locations I will travel to in order to pack more efficiently and do better
route planning. This is especially useful in the winter where I try to
anticipate lake ice and snow conditions.

I find the way Environment Canada shows information about weather stations
painful to use when trying to find the best station to draw data from. By
overlaying the active stations on a map I can more easily determine the best
choice. The url field then makes it easy to jump to the data.

Below is a list of maps I have created using output from this script
* Dec 2020 https://www.google.com/maps/d/u/0/edit?mid=1yIqZFfyOTgg509UNoe03iD_1ht8&usp=sharing

## Notes
The code assumes yesterday's data is always available. Weather Canada does not produce a list of stations
until the end of the day is PST so this code always uses PST time to identify what day it is.

## Disclaimers
This is not an officially supported Google product.