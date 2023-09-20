from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.views.decorators.cache import cache_page

# Create your views here.


def extract_weather_data(text):
    """Extracts weather data from a text string.

    Args:
        text: A text string containing the weather data.

    Returns:
        A dictionary containing the extracted weather data.
    """
    # Split the text into a list of strings.
    strings = text.split()
    # Extract the station name.
    station = strings[2]

    # Extract the last observation time.
    last_observation = strings[0] + " at " + strings[1] + " GMT"

    temp1, temp2 = strings[8].split("/")

    if "M" in temp1:
        temp1 = temp1.replace("M", "-")
    if "M" in temp2:
        temp2 = temp2.replace("M", "-")
    temperature = temp1 + " C (" + temp2 + " F)"

    # Extract the wind direction and speed.
    wind_direction = strings[8]
    wind_speed = strings[7] + " mph (" + strings[6] + " knots)"

    # Create a dictionary to store the extracted weather data.
    weather_data = {}
    weather_data["station"] = station
    weather_data["last_observation"] = last_observation
    weather_data["temperature"] = temperature
    weather_data["wind"] = wind_direction + " at " + wind_speed

    return weather_data
    # {
    #     'station': 'KSGS',
    #     'last_observation': '2017/04/11 at 16:00 GMT',
    #     'temperature': '-1 C (30 F)',
    #     'wind': 'S at 6 mph (5 knots)'
    # }

# url = "http://tgftp.nws.noaa.gov/data/observations/metar/stations/KHUL.TXT"
# stationsUrl = "http://tgftp.nws.noaa.gov/data/observations/metar/stations/"

def index(request):
    try:
        return JsonResponse({"status": "alive"})
    except Exception as e:
        return JsonResponse({"error": e})


def ping(request):
    return JsonResponse({"message": "pong"})


@cache_page(60 * 5)
def info(request):
    r = request.GET.get('scode')
    if r:
        url = "http://tgftp.nws.noaa.gov/data/observations/metar/stations/"
        data = requests.get(f'{url}{r}.TXT')
        result = extract_weather_data(data.text)
        return JsonResponse({"data": result})

    return JsonResponse({"data": None})
