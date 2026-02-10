import logging
import traceback
from typing import Callable

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

# from infrastructure.exceptions.exceptions import (
#     AuthenticationError,
#     InfrastructureError,
# )
from src.shared.web_models import BaseWebOutputModel
from src.shared_kernel.exceptions import (
    DomainError,
    EntityNotFoundError,
    EntityValidationError,
    EntityAlreadyExistError,
    PermissionDeniedError,
)
# from src.users.domain.exceptions.exceptions import UserPasswordInvalidError

CORE_EXCEPTIONS_TO_STATUS_CODES = {
    EntityNotFoundError: status.HTTP_404_NOT_FOUND,
    EntityValidationError: status.HTTP_422_UNPROCESSABLE_CONTENT,
    EntityAlreadyExistError: status.HTTP_403_FORBIDDEN,
    PermissionDeniedError: status.HTTP_403_FORBIDDEN,
    # PermissionDeniedException: status.HTTP_403_FORBIDDEN,
    # AuthorizationException: status.HTTP_403_FORBIDDEN,
    # AuthException: status.HTTP_401_UNAUTHORIZED,
    # ExternalServiceException: status.HTTP_502_BAD_GATEWAY,
}

LOGICAL_EXCEPTIONS_TO_STATUS_CODES = {
    # Everything that not specified as 400 is 500. We haven't figured out yet which exceptions should be 400.
    # We will put them here as they come up.
    # UserPasswordInvalidError: status.HTTP_401_UNAUTHORIZED,
}

# INFRASTRUCTURE_EXCEPTIONS_TO_STATUS_CODES = {
#     AuthenticationError: status.HTTP_401_UNAUTHORIZED,
# }

EXCEPTIONS_TO_STATUS_CODES = {
    **CORE_EXCEPTIONS_TO_STATUS_CODES,
    **LOGICAL_EXCEPTIONS_TO_STATUS_CODES,
    # **INFRASTRUCTURE_EXCEPTIONS_TO_STATUS_CODES,
}

logger = logging.getLogger(__name__)


def build_error_extra(exc: Exception) -> dict[str, str]:
    return {
        "error_type": type(exc).__name__,
        "error_message": str(exc),
        "error_traceback": "".join(
            traceback.TracebackException.from_exception(exc).format()
        ),
    }


def create_processing_domain_exception_handler(status_code: int) -> Callable:
    def _handler(_: Request, exc: DomainError) -> JSONResponse: #| InfrastructureError) -> JSONResponse:
        if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
            logger.error("Internal server error", extra=build_error_extra(exc))
        else:
            logger.info("Client error", extra=build_error_extra(exc))

        return JSONResponse(
            status_code=status_code,
            content=BaseWebOutputModel(
                success=False,
                error_code=type(exc).__name__,
                error_message=exc.ru_detail,
            ).model_dump(),
        )

    return _handler


def handle_exceptions(application: FastAPI):
    for exception, status_code in EXCEPTIONS_TO_STATUS_CODES.items():
        application.exception_handler(exception)(
            create_processing_domain_exception_handler(status_code=status_code)
        )

    @application.exception_handler(RequestValidationError)
    def validation_error_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.error("Validation error", extra=build_error_extra(exc))
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=BaseWebOutputModel(
                success=False,
                error_code=type(exc).__name__,
                error_message=str(exc),
            ).model_dump(),
        )

    @application.exception_handler(Exception)
    def unknown_error_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.error("Unhandled exception", extra=build_error_extra(exc))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=BaseWebOutputModel(
                success=False,
                error_code=type(exc).__name__,
                error_message=(
                    "Произошла непредвиденная ошибка."
                    if not hasattr(exc, "ru_detail")
                    else getattr(exc, "ru_detail")
                ),
            ).model_dump(),
        )
