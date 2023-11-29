from typing import Dict, List

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.gis.geos import Point

from .parsers import CsvUploadParser
from .serializers import AddressSerializer
from .models import Address
from  .forms import SearchForm

from project.settings import DADATA_CLIENT

import logging

logging.getLogger(__name__)


@api_view(['POST'])
@parser_classes([JSONParser, CsvUploadParser])
def address_post(request):
    # NOTE CsvUploadParser
    # :returns {address:[Dict[CSV_HEADER_FIELD, Value]]}: - that's equal default JSON formatter.

    # Get request data
    if "address" not in request.data:
        return Response(data={'status': 'error',
                              'message': "Expect key: 'address' - Address or list of Address or csv file!"},
                        status=status.HTTP_400_BAD_REQUEST)

    errors: List[Dict] = []

    addresses = request.data['address']

    # All to list of Dict:AddressPrototype
    if isinstance(addresses, dict):
        addresses = [addresses]

    # Validation
    # TODO serializer(many=True)
    # serializer = AddressSerializer(data=addresses, many=True)
    # serializer.is_valid()
    for item in addresses:
        # NOTE hardcoded. Need refactor with serializer(many=True)
        for key in item:
            if item[key] == '':
                item[key] = None

        # Postgis Point init
        if item.get('geo_lat', None) is not None and item.get('geo_lon', None) is not None:
            item['location'] = Point(float(item['geo_lat']), float(item['geo_lon']))

        serializer = AddressSerializer(data=item)
        if serializer.is_valid():
            # Create objects
            serializer.save()
            logging.debug({'OBJECT_SAVED': {'type': 'Address',
                                            'data': serializer.validated_data}})
        else:
            logging.info({'FAIL_OBJECT_CREATION': {'type': 'Address',
                                                   'data': item,
                                                   'errors': serializer.errors}})
            error = {'INVALID_DATA': serializer.errors,
                     'address': serializer.data}
            errors.append(error)

    # Standard response cases
    response_data = {'status': '',
                     'total': len(addresses),
                     'updated': 0,
                     'errors': errors}
    if len(errors) == len(addresses):
        response_data['status'] = 'invalid data'
        response_status = status.HTTP_400_BAD_REQUEST
    elif len(errors) > 0:
        response_data['status'] = 'with errors'
        response_data['updated'] = len(addresses) - len(errors)
        response_status = status.HTTP_206_PARTIAL_CONTENT
    else:
        response_data['status'] = 'ok'
        del response_data['updated']
        del response_data['errors']
        response_status = status.HTTP_200_OK

    return Response(data=response_data,
                    status=response_status)


@api_view(['POST'])
@parser_classes([JSONParser])
def get_clean_address(request):
    # TODO celery task
    if 'query' not in request.data:
        return Response(data={'status': 'error',
                              'message': "Request must contain task and query strings!"},
                        status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(request.data['query'], str):
        return Response(data={'status': 'error',
                              'message': f"Expect string, but got {request.data['query']}!",
                              },
                        status=status.HTTP_400_BAD_REQUEST)

    if request.data['query'].strip() == '':
        return Response(data={'status': 'error',
                              'message': f"Expect address but got empty string!",
                              },
                        status=status.HTTP_400_BAD_REQUEST)

    # TODO before request - check cache and search in DB
    # TODO DB search for searching preview on page.
    address = DADATA_CLIENT.clean(name="address", source=request.data['query'])
    if 'result' in address:
        address['address'] = address['result']
    # location processing
    if address.get('geo_lat', None) is not None and address.get('geo_lon', None) is not None:
        address['location'] = Point(float(address['geo_lat']), float(address['geo_lon']))

    if 'qc' not in address:
        # TODO for handling API errors need more info!
        logging.error({'INTEGRATION_ERROR': address})
        return Response(data={'status': 'error',
                              'message': 'Geocoding service error!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if address['qc'] == 0 or ((address['qc'] == 3 or address['qc'] == 1) and request.data['force']):
        # All ok or User apply force for ignore warnings
        serializer = AddressSerializer(data=address)

        if serializer.is_valid():
            # Create objects
            serializer.save()
            logging.debug({'OBJECT_SAVED': {'type': 'Address',
                                            'data': serializer.validated_data}})
            return Response(data={'status': 'ok',
                                  'address': serializer.validated_data},
                            status=status.HTTP_201_CREATED)
        else:
            # TODO IMPORTANT handling
            logging.error({'INTEGRATION_ERROR': {'comment': "get valid response from DaData but data is invalid",
                                                 'data': address,
                                                 'errors': serializer.errors},
                           'tag': 'IMPORTANT'})
    elif address['qc'] == 2:
        return Response(data={'status': 'error',
                              'message': 'Empty or trash data!'},
                        status=status.HTTP_400_BAD_REQUEST)
    elif address['qc'] == 1 or address['qc'] == 3:
        # TODO cache request
        logging.warning({'ADDRESS_CLEAN_WARNING': address})
        return Response(data={'status': 'warning',
                              'message': 'Request has unused parts or address has alternatives!\n'
                                         'To ignore this warning use \'"force": True\' option. '})
    else:
        # TODO for handling API errors need more info!
        logging.error({'INTEGRATION_ERROR': {'comment': 'unhandled error from DaData',
                                             'query': request.data['query'],
                                             'data': address},
                       'tag': 'IMPORTANT'})
        return Response(data={'status': 'error',
                              'message': 'Geocoding service error!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def search_address(request):
    """TODO Optimize in future."""
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            search_result = Address.objects.annotate(
                rank=SearchRank(SearchVector('address', config='russian'),
                                SearchQuery(query, config='russian'))).filter(rank__gte=0.3).order_by("-rank")[:5]
            return Response(data=AddressSerializer(search_result, many=True).data,
                            status=status.HTTP_200_OK)
