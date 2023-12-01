"""Geocoding services"""
from typing import Any, Dict, Literal, Union

from rest_framework import status

from .serializers import AddressSerializer

from .errors import (RequestEmptyError,
                     ResponseEmptyError,
                     DadataResponseHandlingError,
                     RequestNotObviousWarning)

import logging

logging.getLogger(__name__)


def parse_dadata_response(address, force: bool = False) -> Dict[Union[Literal["data"], Literal["status"]], Any]:
    """Handling Dadata.clean() response
    Params:
        :param address: Dadata.clean() -> response
        :param force: flag to ignore warnings.
        :return:
    """
    if 'qc' not in address:
        # TODO for handling API errors need more info!
        logging.error({'EMPTY_DADATA_RESPONSE': address})
        raise ResponseEmptyError()

    if address['qc'] == 0 or ((address['qc'] == 3 or address['qc'] == 1) and force):
        # All ok or User apply force for ignore warnings
        serializer = AddressSerializer(data=address)
        if serializer.is_valid():
            # Create objects
            serializer.save()
            logging.debug({'OBJECT_SAVED': {'type': 'Address',
                                            'data': serializer.validated_data}})

            # ALL OK
            return {'data': serializer.validated_data,
                    'status': status.HTTP_201_CREATED}
        else:
            logging.debug({"FROM_DADATA_VALIDATION_FAILED": serializer.errors})

            # TODO handle fias_id is not unique
            if serializer.errors:
                logging.warning({"FROM DADATA VALIDATION FAILED"})
                # ALL OK BUT RECORD ALREADY EXIST
                return {'data': address,
                        'status': status.HTTP_200_OK}
            else:
                # TODO IMPORTANT handling
                logging.error({'INTEGRATION_ERROR': {'comment': "get valid response from DaData but data is invalid",
                                                     'data': address,
                                                     'errors': serializer.errors},
                               'tag': 'IMPORTANT'})
                raise DadataResponseHandlingError()

    elif address['qc'] == 2:
        raise RequestEmptyError()
    elif address['qc'] == 1 or address['qc'] == 3:
        # TODO cache request
        logging.warning({'ADDRESS_CLEAN_WARNING': address})
        raise RequestNotObviousWarning()
    else:
        # TODO for handling API errors need more info!
        logging.error({'INTEGRATION_ERROR': {'comment': 'unhandled error from DaData',
                                             'data': address},
                       'tag': 'IMPORTANT'})
        raise DadataResponseHandlingError()
