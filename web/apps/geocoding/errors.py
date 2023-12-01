"""Geocoding errors"""


class BaseError(Exception):
    """Base error class for Geocoding"""
    pass


class DadataIntegrationError(BaseError):
    """Base error class for Dadata response handling"""
    pass


class ResponseEmptyError(DadataIntegrationError):
    """Response from dadata was empty."""
    def __str__(self):
        return "Unhandled error from DaData!"


class DadataResponseHandlingError(DadataIntegrationError):
    """Error handling response from dadata"""
    def __str__(self):
        return "Invalid response from related server."


class RequestEmptyError(DadataIntegrationError):
    """Error request from dadata"""
    def __str__(self):
        return "Empty or trash data!"


class RequestNotObviousWarning(DadataIntegrationError):
    """Unused parts in request or result address has alternatives"""
    def __str__(self):
        return ('Request has unused parts or address has alternatives!\n'
                'To ignore this warning use \'"force": True\' option. ')
