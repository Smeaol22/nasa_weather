from datetime import datetime

from pandas import DataFrame

from src.enumeration import OutputFormat
from src.object.WeatherDay import WeatherDay


def convert_date_to_timestamp(date_to_convert):
    """
        This function is useful to convert date (YYYYmmdd) to timestamp
    Args:
        date_to_convert (str): date (YYYYmmdd) to be converted in timestamp

    Returns:
        (timestamp): date_to_convert converted in timestamp

    """
    return int(datetime.strptime(date_to_convert, '%Y%m%d').timestamp())


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


def average_regional_data(weather_data, params, output_format):
    """
        This function is useful to aggregate and average regional weather data for each day
    Args:

        weather_data (list): list of dict containing weather data
        params (str): list of requested params
        output_format (OutputFormat): type of return, see output_format.py for value

    Returns:
        (list(WeatherDay)) / (dataframe) / (dict): weather data zonal average, one for each requested days
    """

    params_list = eval("['" + params.replace(",", "','") + "']")
    weather_data_avg = {}
    nb_points = len(weather_data)
    for param in params_list:
        weather_data_avg[param] = [0] * nb_points
    weather_data_avg['date'] = list(weather_data[0]['properties']['parameter']['RH2M'].keys())

    for weather_point in weather_data:
        wp_parameter = weather_point['properties']['parameter']
        for param in params_list:
            weather_data_avg[param] = [x + y for x, y in
                                       zip(weather_data_avg[param], list(wp_parameter[param].values()))]
    for param in params_list:
        weather_data_avg[param] = [x / nb_points for x in weather_data_avg[param]]

    if output_format == OutputFormat.WEATHER_DAY_LIST:
        weather_days_data = []
        for index, date in enumerate(weather_data_avg['date']):
            weather_days_data.append(
                WeatherDay(convert_date_to_timestamp(date), weather_data_avg['RH2M'][index],
                           weather_data_avg['PRECTOT'][index],
                           weather_data_avg['WS2M'][index], weather_data_avg['ALLSKY_SFC_SW_DWN'][index],
                           weather_data_avg['T2M_MIN'][index], weather_data_avg['T2M_MAX'][index],
                           weather_data_avg['T2M'][index]))
    elif output_format == OutputFormat.DATAFRAME:
        date_s = [convert_date_to_timestamp(date) for date in weather_data_avg['date']]
        weather_days_data = DataFrame(
            {'date': date_s, 'relative_humidity': weather_data_avg['RH2M'],
             'precipitation': weather_data_avg['PRECTOT'], 'wind_speed': weather_data_avg['WS2M'],
             'solar_radiation': weather_data_avg['ALLSKY_SFC_SW_DWN'], 'temp_min': weather_data_avg['T2M_MIN'],
             'temp_max': weather_data_avg['T2M_MAX'], 'temp_avg': weather_data_avg['T2M']},
            columns=['date', 'relative_humidity', 'precipitation', 'wind_speed', 'solar_radiation', 'temp_min',
                     'temp_max',
                     'temp_avg'])

    elif output_format == OutputFormat.DICT:
        weather_days_data = weather_data_avg
    else:
        raise ValueError(f'{output_format} is not acceptable as output_format')
    return weather_days_data
