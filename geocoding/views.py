from typing import Dict, List

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response

from .parsers import CsvUploadParser
from .serializers import AddressSerializer


import logging

logging.getLogger(__name__)


@api_view(['POST'])
@parser_classes([JSONParser, CsvUploadParser])
def address_post(request):
    # Get request data
    if "address" not in request.data:
        return Response(data={'status': 'error',
                              'message': "Expect key: 'address' - Address or list of Address or csv file!"},
                        status=status.HTTP_400_BAD_REQUEST)

    data: List[Dict] = []
    errors: List[Dict] = []

    # NOTE CsvUploadParser
    # :returns {address:[Dict[CSV_HEADER_FIELD, Value]]}: - that's equal default JSON format.
    if isinstance(request.data['address'], dict):
        # JSON single address
        data = [request.data['address']]
    elif isinstance(request.data['address'], list):
        # JSON list of address
        data = request.data['address']

    # Validation

    for item in data:
        # TODO handling for set default value
        if item['foundation_year'] == '':
            del item['foundation_year']

        serializer = AddressSerializer(data=item)
        logging.info("before validation")
        if serializer.is_valid():
            logging.debug(f'VALID: {str(item)[:30]}...')
            # Create objects
            serializer.save()
        else:
            logging.warning(f'INVALID: {str(item)[:30]}...')
            error = {'INVALID_DATA': serializer.errors,
                     'address': serializer.data}
            errors.append(error)

    # Standard response cases
    if len(errors) == len(data):
        response_data = {'status': 'invalid data',
                         'total': len(data),
                         'updated': 0,
                         'errors': errors}
        return Response(data=response_data,
                        status=status.HTTP_400_BAD_REQUEST)
    elif len(errors) > 0:
        response_data = {'status': 'with errors',
                         'total': len(data),
                         'updated': len(data) - len(errors),
                         'errors': errors}
        return Response(data=response_data,
                        status=status.HTTP_206_PARTIAL_CONTENT)
    else:
        response_data = {'status': 'ok',
                         'total': len(data)}
        return Response(data=response_data,
                        status=status.HTTP_201_CREATED)
