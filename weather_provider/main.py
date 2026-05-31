from abc import ABC, abstractmethod
import requests

class WeatherAbstract(ABC):
    @abstractmethod
    def get_current_weather(self, lat, lon):
        pass
    
    
class OpenWeatherProvider(WeatherAbstract):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key):
        self.api_key = api_key

    def get_current_weather(self, lat, lon):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        normalize_data = {"temp": float(response.json()["main"]["temp"]) - 273.15,
                          "humidity": response.json()["main"]["humidity"]}

        return normalize_data
    
    
    
class OpenMeteoProvider(WeatherAbstract):
    base_url = "https://api.open-meteo.com/v1/forecast"

    def get_current_weather(self, lat, lon):
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m"
        }
        response = requests.get(self.base_url, params=params)
        normalize_data = {"temp": response.json()["current"]["temperature_2m"],
                          "humidity": response.json()["current"]["relative_humidity_2m"]}
        return normalize_data
    
#search my current lat and lan
    
# provider = OpenWeatherProvider("token")
# print(provider.get_current_weather(lat=35.82472320684597, lon=51.00105750513447))

provider = OpenMeteoProvider()
print(provider.get_current_weather(lat=35.82472320684597, lon=51.00105750513447))