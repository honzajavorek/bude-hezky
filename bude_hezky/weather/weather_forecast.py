import datetime
import requests

API_URL = 'http://api.openweathermap.org'
API_OPTION_KEY = 'appid'
DAY_START_AT_HOUR = 7
DAY_ENDS_AT_HOUR = 18

def get_sunny_like_hours(all_forecasts): 
    sunny_like_hours = []
    tomorrow_reached = False
    tomorrow_date = datetime.date.today() + datetime.timedelta(days=1)

    for forecast in all_forecasts:
        datetime_of_forecast = datetime.datetime.fromtimestamp(forecast.get('dt'))
        weather_id = forecast.get('weather')[0].get('id')
        hour_of_forecast = datetime_of_forecast.hour

        if hour_of_forecast < DAY_START_AT_HOUR or hour_of_forecast > DAY_ENDS_AT_HOUR:
            continue
        elif datetime_of_forecast.date() == tomorrow_date:
            tomorrow_reached = True
            if weather_id in [800, 801, 802]:
                sunny_like_hours.append(hour_of_forecast)
        elif tomorrow_reached:
            break

    return sunny_like_hours 

def get_forecasts_for_city(api_key, city_name):
    response = requests.get(
        f'{API_URL}/data/2.5/forecast/?q={city_name}&mode=json', 
        params={API_OPTION_KEY: api_key}
    )
    response.raise_for_status()

    return response.json().get('list')
