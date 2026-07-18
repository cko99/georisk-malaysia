"""
core/exceptions.py

Domain-specific exceptions raised by the Service layer and translated
into standardized HTTP responses by the API layer / global exception
handlers registered in `app.py`.
"""


class ExternalAPIError(Exception):
    """
    Raised whenever a call to an upstream provider (data.gov.my) fails,
    times out, or returns a non-success HTTP status code.
    """

    def __init__(self, module: str, message: str, status_code: int = 503):
        self.module = module
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ExternalAPITimeoutError(ExternalAPIError):
    """Raised when the upstream provider does not respond within the configured timeout."""

    def __init__(self, module: str, message: str = "External API unavailable"):
        super().__init__(module=module, message=message, status_code=503)


class ExternalAPIInvalidResponseError(ExternalAPIError):
    """Raised when the upstream provider returns an unparsable or malformed payload."""

    def __init__(self, module: str, message: str = "External API unavailable"):
        super().__init__(module=module, message=message, status_code=503)
