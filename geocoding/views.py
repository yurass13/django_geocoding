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
