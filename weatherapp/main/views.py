import os
from django.shortcuts import render
import httpx
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
WEATHER_API_TOKEN = os.getenv("WEATHER_API_TOKEN")

# Create your views here.

def homepage(request):
    return render(request, 'main/index.html')

def page_not_found_view(request, exception):
    return render(request, 'main/404.html', status=404)

def get_weather_data_by_city_name(request):
    city = request.POST.get('city')
    errors = []
    if not WEATHER_API_TOKEN:
        errors.append('Weather API token is missing.')
        return render(request, 'main/index.html', {'errors': errors})
    #validation
    if not city or len(city.strip()) > 50: #no city name should be more than 50 chars, just a safeguard
        errors.append('City name is required and should be less than 50 characters.')
        return render(request, 'main/index.html', {'errors': errors})

    response = httpx.get(f'https://api.openweathermap.org/data/2.5/weather?q={city.strip()}&appid={WEATHER_API_TOKEN}')

    if response.status_code == 200:
        data = response.json()
        data['main']['temp'] = round(data['main']['temp'] - 273.15, 2)  #kelvin to c
        return render(request, 'main/index.html', {'data': data})
    
    errors.append('City not found.')
    print(response.text)
    return render(request, 'main/index.html', {'errors': errors})