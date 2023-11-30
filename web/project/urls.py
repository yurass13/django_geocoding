from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.map.urls', namespace='apps.map')),
    path('geocoding/api/v1/', include('apps.geocoding.urls', namespace='apps.geocoding')),
]
