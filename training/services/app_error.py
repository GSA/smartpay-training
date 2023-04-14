class AppError(Exception):
    """
    A general-purpose class to communicate error conditions. Although this
    class is not specific to web API endpoints, the error `code` given to this
    class should ideally correspond to HTTP error status codes. This makes it
    easier for the API endpoints to translate the error into the appropriate
    HTTP error response.
    """

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
