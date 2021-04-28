from enum import Enum


class OutputFormat(Enum):
    DICT = "dict"
    DATAFRAME = "dataframe"
    WEATHER_DAY_LIST = "weather_day_list"


class RegionalOutput(Enum):
    RAW = "raw"
    AVERAGE = "average"
