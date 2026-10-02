from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Self

from loguru import logger

LogMethod = Callable[[dict[str, str]], None]


def fetch_logger_type(log_level: str) -> LogMethod:
    """Fetches the corresponding logger method based on log_level string."""
    return getattr(logger, log_level.lower(), logger.info)


def bind_logger(log_level: str, log_data: dict[str, str]) -> LogMethod:
    bound_logger = logger.bind(log_data=log_data).opt(depth=3)
    return getattr(bound_logger, log_level)


class LogType(StrEnum):
    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    SUCCESS = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

    def raise_error(
        self, exception_type: type[BaseException], response: str
    ) -> None:
        LogRenderer(self.value).handle_exception(exception_type, response)

    def write(self, response: str) -> None:
        LogRenderer(self.value).write_log(response)


@dataclass(frozen=True, slots=True)
class LogRenderer:
    log_level: str

    def bind(self, log_data: dict[str, str]) -> LogMethod:
        return bind_logger(self.log_level, log_data)

    def handle_exception(
        self, exception_type: type[BaseException], response: str
    ):
        """Logs the error and raises the provided exception type."""
        (
            ExceptionRenderer(self.log_level, exception_type, response)
            .log_report()
            .raise_error()
        )

    def write_log(self, response):
        """Writes a simple structured log message."""
        report_log = {"status": self.log_level, "response": response}

        self.bind(report_log)(response)


@dataclass(frozen=True, slots=True)
class ExceptionRenderer:
    log_level: str
    exception_type: type[BaseException] | None
    response: str

    @property
    def logger_type(self) -> LogMethod:
        return fetch_logger_type(self.log_level)

    @property
    def report_log(self) -> dict[str, str]:
        struct = {"status": self.log_level}

        if self.exception_type is not None:
            struct["exception_type"] = self.exception_type.__name__

        struct["response"] = self.response
        return struct

    def bind(self, log_data: dict[str, str]) -> LogMethod:
        return bind_logger(self.log_level, log_data)

    def log_report(self) -> Self:
        self.bind(self.report_log)(self.response)

        return self

    def raise_error(self) -> Self:
        if self.exception_type:
            raise self.exception_type(self.report_log)
        return self
