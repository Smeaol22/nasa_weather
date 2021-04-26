from datetime import datetime

from pandas import DataFrame

from src.object.WeatherDay import WeatherDay


def convert_date_to_timestamp(date_to_convert):
    """
        This function is useful to convert date (YYYYmmdd) to timestamp
    Args:
        date_to_convert (str): date (YYYYmmdd) to be converted in timestamp

    Returns:
        (timestamp): date_to_convert converted in timestamp

    """
    return datetime.strptime(date_to_convert, '%Y%m%d').timestamp()


def convert_nasa_response_to_dataframe(weathers_data):
    """
        This function is useful to load weathers_data into a dataframe
    Args:
        weathers_data (dict): dictionary containing all weather data obtain from power NASA:

    Returns:
        (dataframe): Dataframe with all weather data over requested time lapse
    """
    date = [convert_date_to_timestamp(day_date) for day_date in list(weathers_data['RH2M'].keys())]
    relative_humidity = list(weathers_data['RH2M'].values())
    precipitation = list(weathers_data['PRECTOT'].values())
    wind_speed = list(weathers_data['WS2M'].values())
    solar_radiation = list(weathers_data['ALLSKY_SFC_SW_DWN'].values())
    temp_min = list(weathers_data['T2M_MIN'].values())
    temp_max = list(weathers_data['T2M_MAX'].values())
    temp_avg = list(weathers_data['T2M'].values())
    return DataFrame(
        {'date': date, 'relative_humidity': relative_humidity, 'precipitation': precipitation, 'wind_speed': wind_speed,
         'solar_radiation': solar_radiation, 'temp_min': temp_min, 'temp_max': temp_max, 'temp_avg': temp_avg},
        columns=['date', 'relative_humidity', 'precipitation', 'wind_speed', 'solar_radiation', 'temp_min', 'temp_max',
                 'temp_avg'])


def convert_nasa_response_to_weather_day_list(weathers_data):
    """
        This function is useful to load weathers_data into a list of WeatherDay
    Args:
        weathers_data (dict): dictionary containing all weather data obtain from power NASA

    Returns:
        weather_days_list (list(weatherDay)): list of weatherDay
    """
    weather_days_list = []
    for day in weathers_data['RH2M']:
        day_timestamp = convert_date_to_timestamp(day)
        relative_humidity = weathers_data['RH2M'][day]
        precipitation = weathers_data['PRECTOT'][day]
        wind_speed = weathers_data['WS2M'][day]
        solar_radiation = weathers_data['ALLSKY_SFC_SW_DWN'][day]
        temp_min = weathers_data['T2M_MIN'][day]
        temp_max = weathers_data['T2M_MAX'][day]
        temp_avg = weathers_data['T2M'][day]

        weather_days_list.append(
            WeatherDay(day_timestamp, relative_humidity, precipitation, wind_speed, solar_radiation, temp_min, temp_max,
                       temp_avg))
    return weather_days_list
