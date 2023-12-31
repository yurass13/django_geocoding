"""Map views"""
import json
import requests

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.shortcuts import redirect, render, reverse

from apps.geocoding.models import Address

from .forms import SearchAddress
from .utils import get_html_map

import logging

logging.getLogger(__name__)


def maps(request):
    """Returns Homepage with map and searching form."""
    # TODO DB search preview on page.

    map_config = {}
    if request.method == "POST":
        form = SearchAddress(request.POST)
        if form.is_valid():
            # not accuracy but works TODO to refactor
            data = json.dumps({'query': form.cleaned_data['address']})
            logging.debug({"TO_CLEAN": data})
            headers = {'Content-Type': 'application/json'}
            response = requests.post('http://' + request.get_host() + reverse('apps.geocoding:address_clean'),
                                     data=data,
                                     headers=headers)
            data = json.loads(response.content)
            logging.debug({'FROM_ADDRESS_CLEAN': data})

            # API response handling
            if response.status_code in [200, 201]:
                map_config['target'] = (data['address'],
                                        data['geo_lat'],
                                        data['geo_lon'],
                                        int(form.cleaned_data['radius']) * 1000)

                # Get Markers
                # NOTE Not optimal
                # TODO need create polygon area and check address.location in area (need tests)
                current_point = Point(x=float(data['geo_lat']),
                                      y=float(data['geo_lon']),
                                      srid=4326)

                address_qs = Address.objects.annotate(distance=Distance('location', current_point)).\
                    filter(distance__lte=int(form.cleaned_data['radius']) * 1000)
                # TODO Place for serializer?
                map_config['cities'] = [(city.address, city.geo_lat, city.geo_lon, None)
                                        for city in address_qs]

    else:
        form = SearchAddress()

    logging.debug({'MAP_CONFIG': map_config})

    # Render map
    html_map = get_html_map(**map_config)
    return render(request,
                  template_name='map/map.html',
                  context={'title': 'Geo Search',
                           'map': html_map,
                           'form': form})


def index(request):
    """Redirect to the views.map()"""
    return redirect("/map/")
