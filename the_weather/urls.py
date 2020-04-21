from the_weather import views
from django.urls import path

app_name = 'the_weather'

urlpatterns = [
    path('', views.index, name='home'),
    path('<city_name>/delete', views.delete, name='delete'),
]