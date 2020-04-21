import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=d2ad988e3aea888bca35fc4b05349dd6'
    # datetime module is a class, x is its object

    # if that object is already created in the database then return already created
    # if not, create that object

    if request.method == "POST":
        # if object exists with name = requested POST data ['name'] key
        if City.objects.filter(name=request.POST['name']).exists():
            messages.info(request,'City already exists')
            return redirect('the_weather:home')
        else:
            form = CityForm(request.POST)
            form.save()


    all_city = City.objects.all()
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
        # so that we can display that list on the homepage

        weather_list.append(city_weather)
    form = CityForm()
    context = {'weather_list': weather_list}
    return render(request, 'the_weather/index.html', context=context)
