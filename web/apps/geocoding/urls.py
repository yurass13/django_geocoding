from django.urls import path
from . import views


app_name = 'apps.geocoding'

urlpatterns = [
    path('address/', views.address_post, name="address_post"),
    path('address/clean/', views.get_clean_address, name="address_clean"),
    path('address/search/', views.search_address, name="address_search")
]
