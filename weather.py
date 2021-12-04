import pyowm
import requests

owm = pyowm.OWM('01e01f9395c0b538f90452868fc31adf')

res = requests.get('https://ipinfo.io/')
data = res.json()

city = data['city']

loc = owm.weather_manager().weather_at_place(city)
weather = loc.weather

def temp():
    temp = weather.temperature(unit='celsius')
    cleaned_temp_data = (int(temp['temp']))
    return cleaned_temp_data

def status():
    status = weather.detailed_status
    return status