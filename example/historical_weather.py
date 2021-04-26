from src.main import retrieve_point_weather_data

# Example based on https://power.larc.nasa.gov/docs/tutorials/service-data-request/api/


latitude = 32.929
longitude = -95.770
start_date = 20191215
end_date = 20191230
retrieve_point_weather_data(longitude, latitude, start_date, end_date)
