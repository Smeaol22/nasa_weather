class WeatherDay(object):

    def __init__(self, date, relative_humidity, precipitation, wind_speed, solar_radiation, temp_min, temp_max,
                 temp_avg):
        self.date = date
        self.relative_humidity = relative_humidity  # RH2M
        self.precipitation = precipitation  # PRECTOT
        self.wind_speed = wind_speed  # WS2M
        self.solar_radiation = solar_radiation  # ALLSKY_SFC_SW_DWN
        self.temp_min = temp_min  # T2M_MIN
        self.temp_max = temp_max  # T2M_MAX
        self.temp_avg = temp_avg  # T2M
