from django.urls import path
from . import views


app_name = 'apps.map'

urlpatterns = [
    path('map/', views.maps, name='map'),
    path('', views.index, name='index'),
]
