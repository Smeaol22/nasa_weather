import json
import time

import requests

from src.enumeration import RegionalOutput, OutputFormat
from src.error import NasaRequestError
from src.utils import convert_nasa_response_to_weather_day_list, convert_nasa_response_to_dataframe, \
    average_regional_data

BASE_URL = r"https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py?" \
           r"request=execute&identifier={identifier}&tempAverage=DAILY" \
           r"&parameters={params}&startDate={start_date}&endDate={end_date}{location}" \
           r"&outputList=JSON&userCommunity=SSE"

PARAMS = 'RH2M,PRECTOT,WS2M,ALLSKY_SFC_SW_DWN,T2M_MIN,T2M_MAX,T2M'


def retrieve_point_weather_data(longitude, latitude, start_date, end_date, output_format=OutputFormat.DATAFRAME):
    """
        This function is useful to retrieve weather data at a point
    Args:
        longitude (int): longitude of the point to retrieve weather data
        latitude (int): latitude of the point to retrieve weather data
        start_date (int): first day to retrieve weather data
        end_date (int): last day to retrieve weather data
        output_format (OutputFormat): type of return, see output_format.py for value

    Returns:
        (list(WeatherDay)) / (dataframe) / (dict): weather data, one for each requested days
    """

    location = f"&lat={latitude}&lon={longitude}"
    identifier = "SinglePoint"
    response = requests.get(
        BASE_URL.format(identifier=identifier, location=location, start_date=start_date,
                        end_date=end_date, params=PARAMS))
    if response.status_code >= 200 or response.status_code < 300:
        weathers_data = json.loads(response.content.decode('utf-8'))['features'][0]['properties']['parameter']
        if output_format == OutputFormat.WEATHER_DAY_LIST:
            weather_days_data = convert_nasa_response_to_weather_day_list(weathers_data)
        elif output_format == OutputFormat.DATAFRAME:
            weather_days_data = convert_nasa_response_to_dataframe(weathers_data)
        elif output_format == OutputFormat.DICT:
            weather_days_data = weathers_data
        else:
            raise ValueError(f'{output_format} is not acceptable as output_format')
    else:
        raise NasaRequestError(f"Request failed with code {response.status_code}")
    return weather_days_data


def retrieve_regional_weather_data(box, start_date, end_date, regional_output=RegionalOutput.AVERAGE,
                                   output_format=OutputFormat.DATAFRAME, data_request_delay=10):
    """
        This function is useful to retrieve weather data on a rectangle/square area
    Args:
        box (tuple): tuple containing pair of lat/long of opposite rectangle or square corner
        start_date (int): first day to retrieve weather data
        end_date (int): last day to retrieve weather data
        regional_output (RegionalOutput): aggregate and average data or raw data (AVERAGE/RAW)
        output_format (OutputFormat): type of return, see output_format.py for value
        data_request_delay (int): delay before requesting data and submitted request
    Returns:
        (list(WeatherDay)) / (dataframe): weather data, one for each requested days
    """

    location = f"&bbox={box[0]},{box[1]},{box[2]},{box[3]}"
    identifier = "Regional"
    response_to_submission = requests.get(
        BASE_URL.format(identifier=identifier, location=location, start_date=start_date, end_date=end_date,
                        params=PARAMS))
    if response_to_submission.status_code >= 200 or response_to_submission.status_code < 300:
        time.sleep(data_request_delay)
        data_url = json.loads(response_to_submission.content.decode('utf-8'))['outputs']['json']
        response_data = requests.get(data_url, allow_redirects=True)
        weather_data = json.loads(response_data.content.decode('utf-8'))['features']
        if regional_output == RegionalOutput.RAW:
            return weather_data
        elif regional_output == RegionalOutput.AVERAGE:
            return average_regional_data(weather_data, PARAMS, output_format)
        else:
            raise ValueError(f'{regional_output} is not acceptable as regional_output')
    else:
        raise NasaRequestError(f"Request failed with code {response_to_submission.status_code}")
