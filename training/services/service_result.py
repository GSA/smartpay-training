from typing import Any
from training.services import AppError


class ServiceResult():
    """
    A general-purpose class to communicate business logic results back from
    services to API endpoint methods.
    """

    success: bool
    error: AppError
    value: Any

    def __init__(self, value: Any):
        if isinstance(value, AppError):
            self.success = False
            self.error: AppError = value
        else:
            self.success = True
        self.value = value
