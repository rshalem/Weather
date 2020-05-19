import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=d2ad988e3aea888bca35fc4b05349dd6'
    # datetime module is a class, x is its object

    if request.method == "POST":

        # if form.is_valid():
        new_city = request.POST['name']
        r = requests.get(url.format(new_city)).json()
        # city is a match, success 200, checking it in the response 'r' obj
        if r['cod'] == 200:
            if City.objects.filter(name=new_city).exists():
                messages.info(request, 'City exists')
            else:
                form = CityForm(request.POST)
                form.save()
                return redirect('the_weather:home')

        # if city is not a valid city( ie cod = 404)
        else:
            messages.info(request, 'Invalid City')

    # else display all saved city weather
    all_city = City.objects.all()

    # adding all cities with weather detail to this list
    weather_list = []
    for city in all_city:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        # appending city weather for all the city objects to a list
        # so that we can display that list on the homepage, BY LOOPING OVER IN INDEX.HTML
        weather_list.append(city_weather)

    # if request is GET
    form = CityForm()

    context = {'weather_list': weather_list}
    return render(request, 'the_weather/index.html', context=context)


def delete(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('the_weather:home')


