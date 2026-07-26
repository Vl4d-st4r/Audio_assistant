"""import requests
from bs4 import BeautifulSoup
from time import sleep


headers = {
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}



def weather_info():
    url = 'https://www.gismeteo.ru/weather-sankt-peterburg-4079/now'

    response = requests.get(url, headers=headers)
    sleep(1)
    bs = BeautifulSoup(response.text, "lxml")
    sleep(1)
    temp = bs.find('span', 'unit unit_temperature_c').text
    weather = bs.find('div', 'now-desc').text
    humidity = bs.find('div', 'now-info-item humidity').text
    wind = bs.find('div', 'unit unit_wind_m_s').text
    return temp, weather, humidity, wind
"""
import time
day_of_week = time.strftime("%A")
date = time.strftime("%d-%B-%Y")
hour, min = time.strftime("%H:%M").split(':')
print(day_of_week, '\n', date, '\n', hour+':'+min)
print(day_of_week)
print(date)
print("{} hours".format(hour))
print("{} minutes".format(min))
