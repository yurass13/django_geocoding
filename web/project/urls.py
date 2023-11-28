from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('map.urls', namespace='map')),
    path('geocoding/api/v1/', include('geocoding.urls', namespace='geocoding')),
]
