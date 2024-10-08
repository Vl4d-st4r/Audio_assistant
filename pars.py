import requests
from bs4 import BeautifulSoup
from time import sleep


headers = {
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}



def weather_info():
    url = 'https://www.yr.no/en/forecast/daily-table/2-498817/Russia/St.-Petersburg/St%20Petersburg'

    response = requests.get(url)
    sleep(1)
    bs = BeautifulSoup(response.text, "lxml")
    sleep(1)
    temp = bs.find('div', 'feels-like-text').text
    weather = bs.find('img', 'weather-symbol__img').attrs['alt']
    #humidity = bs.find('div', 'now-info-item humidity').text
    wind = bs.find('span', 'wind__container').text
    return temp, weather, wind