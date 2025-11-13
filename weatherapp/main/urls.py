from django.urls import path
from . import views

#urlconfig
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('get_weather_data/', views.get_weather_data_by_city_name,name='get_weather_data')
]