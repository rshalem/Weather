import requests
from django.shortcuts import render
from datetime import datetime

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=d2ad988e3aea888bca35fc4b05349dd6'
    # datetime module is a class, x is its object
    x = datetime.now()
    default_city = 'Chennai'

    city = ""

    if request.method == "POST":
        name = request.POST['name']
        city += name

        # response object 'r'
        r = requests.get(url.format(city)).json()

        city_weather = {
            'date_time': x,
            'city': city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        context = {'city_weather': city_weather}
        return render(request, 'the_weather/index.html', context=context)

    else:
        r = requests.get(url.format(default_city)).json()

        city_weather = {
            'date_time': x,
            'city': default_city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        context = {'city_weather': city_weather}
        return render(request, 'the_weather/index.html', context=context)
