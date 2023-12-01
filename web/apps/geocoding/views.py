"""Geocoding views"""
from typing import Dict, List

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .forms import SearchForm
from .models import Address
from .parsers import CsvUploadParser
from .serializers import AddressSerializer
from .services import parse_dadata_response

from .errors import (RequestEmptyError,
                     ResponseEmptyError,
                     DadataResponseHandlingError,
                     RequestNotObviousWarning)

import logging

logging.getLogger(__name__)


class BadRequestErrorResponse(Response):
    """Base class for HTTP_400_BAD_REQUEST."""
    def __init__(self, message: str = "BadRequest", *args, **kwargs):
        super().__init__(data={'status': 'error',
                               'message': message},
                         status=status.HTTP_400_BAD_REQUEST,
                         *args,
                         **kwargs)


@api_view(['POST'])
@parser_classes([JSONParser, CsvUploadParser])
def address_post(request):
    """
    :param request:
        ContentType: application/json | text/csv
        Data: JSON with key "address" or stream of csv data.
    :returns HttpJsonResponse:
        Valid Response Template:
            Status Codes:
                HTTP_200_OK:                All data ok.
                HTTP_206_PARTIAL_CONTENT:   Data has invalid rows.
                HTTP_400_BAD_REQUEST:       All data invalid.
            Data:
                {
                    "status": Union["ok", "with errors", "invalid data"],
                    "total": int,
                    "updated": int,
                    "errors": [
                        {
                            "INVALID_DATA": {"field_name": ["error messages", ]},
                            "address": {"Address.field": "value"}
                        }
                    ]
                }

        Invalid Response Template:
            Status Code:
                HTTP_400_BAD_REQUEST
            Reason:
                Request must contain "address" key.
            Data:
                {
                    "status": "error",
                    "message": "Expect key: "address" - Address or list of Address or csv file!"
                }
    """
    # NOTE CsvUploadParser
    # :returns {address:[Dict[CSV_HEADER_FIELD, Value]]}: - that's equal default JSON formatter.

    # Get request data
    if "address" not in request.data:
        return Response(data={'status': 'error',
                              'message': "Expect key: \"address\" - Address or list of Address or csv file!"},
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
    """ Clean address using Dadata.clean.
        Responses:

    """
    # TODO celery task
    try:
        # TODO before request - check cache and search in DB
        form = SearchForm(request.data)
        if form.is_valid():
            address = DADATA_CLIENT.clean(name="address", source=form.cleaned_data['query'])    # noqa: F821

            force = True if request.data.get('force', 'false') == 'true' else False
            return Response(**parse_dadata_response(address, force))
        else:
            raise KeyError('Invalid Request Data')

    except (KeyError, TypeError, ValueError) as error:
        logging.info({"WRONG_INPUT": str(error)})
        # NOTE 400
        return BadRequestErrorResponse(message="Expect JSON: {\"query\": \"string\"} ")

    except (DadataResponseHandlingError, ResponseEmptyError) as error:
        # NOTE 500
        return Response(data={"status": "error",
                              "message": str(error)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except (RequestEmptyError, ) as error:
        # NOTE 400
        return BadRequestErrorResponse(message=str(error))
    except (RequestNotObviousWarning, ) as warning:
        return BadRequestErrorResponse(message=str(warning))
