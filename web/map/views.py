from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.shortcuts import redirect, render, reverse
import requests

from geocoding.models import Address

from .forms import SearchAddress
# from .utils import get_html_map


def maps(request):

    html_map = None
    if request.method == "POST":
        form = SearchAddress(request.POST)
        if form.is_valid():
            # not accuracy but works TODO to refactor
            data = {'query': form.cleaned_data['address']}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(reverse('geocoding:address_clean'),
                                    data=data,
                                    headers=headers)

            # API response handling
            if response.staus_code == 201:
                target = (response.data['address']['address'],
                          response.data['address']['geo_lat'],
                          response.data['address']['geo_lon'],
                          form.cleaned_data['radius'])

                # TODO calc zoom constant from current diametr 
                zoom = 4
                current_point = Point(response.data['address']['geo_lat'],
                                      response.data['address']['geo_lon'])

                # Get Markers
                # NOTE Not optimal
                # TODO need create polygon area and check address.location in area (need tests)
                cities = Address.objects.annotate(distance=Distance('location', current_point)).\
                    filter(distance__lte=form.cleaned_data['radius'])
                # TODO Place for serializer?
                # html_map = get_html_map(zoom_start=zoom, target=target, cities=cities)
    else:
        form = SearchAddress()

    if html_map is None:
        # html_map = get_html_map()
        pass
    return render(request,
                  template_name='map/map.html',
                  context={'title': 'Geo Search',
                           'map': html_map,
                           'form': form})


def index(request):
    return redirect("/map/")
