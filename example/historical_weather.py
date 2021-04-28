from src.main import retrieve_point_weather_data, retrieve_regional_weather_data

# Example based on https://power.larc.nasa.gov/docs/tutorials/service-data-request/api/

# example for retrieve weather data at one point
latitude_1 = 4.7649
longitude_1 = -15.6610
start_date = 20191215
end_date = 20191230
retrieve_point_weather_data(longitude_1, latitude_1, start_date, end_date)

# example for retrieve weather data on on box
latitude_2 = 9.2649
longitude_2 = -11.1610
box_example = (latitude_1, longitude_1, latitude_2, longitude_2)
retrieve_regional_weather_data(box_example, start_date, end_date)
