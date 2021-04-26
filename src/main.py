import json

import requests

from src.utils import convert_nasa_response_to_weather_day_list

BASE_URL = r"https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py?" \
           r"request=execute&identifier=SinglePoint&tempAverage=DAILY" \
           r"&parameters={params}&startDate={start_date}&endDate={end_date}&lat={latitude}&lon={longitude}" \
           r"&outputList=JSON&userCommunity=SSE"


def retrieve_point_weather_data(longitude, latitude, start_date, end_date):
    """
        This function is useful to retrieve weather data at a point
    Args:
        longitude (int): longitude of the point to retrieve weather data
        latitude (int): latitude of the point to retrieve weather data
        start_date (int): first day to retrieve weather data
        end_date (int): last day to retrieve weather data

    Returns:
        (list(WeatherDay)): list of weather data, one for each requested days
    """
    params = 'RH2M,PRECTOT,WS2M,ALLSKY_SFC_SW_DWN,T2M_MIN,T2M_MAX,T2M'
    response = requests.get(
        BASE_URL.format(longitude=longitude, latitude=latitude, start_date=start_date,
                        end_date=end_date, params=params))
    if response.status_code >= 200 or response.status_code < 300:
        weathers_data = json.loads(response.content.decode('utf-8'))['features'][0]['properties']['parameter']
        weather_days_list = convert_nasa_response_to_weather_day_list(weathers_data)
    else:
        raise ValueError("error to be changed")
    return weather_days_list


def retrieve_zone_weather_data(polygon, start_date, end_date):
    #    response = requests.get(
    #        BASE_URL.format(polygon, start_date=start_date,
    #                        end_date=end_date))
    #    if response.status_code >= 200 or response.status_code < 300:
    #        weather_data = json.loads(response.content.decode('utf-8'))
    #    else:
    #        raise ValueError("error to be changed")
    return True
