from pathlib import Path

from loguru import logger
from rich.logging import RichHandler

from .log_renderers import LogType


def configure_logger() -> None:
    """Configure the logger with different handlers for console and file output."""

    logger.remove()  # Remove all default loggers

    """ Human-readable stderr for local console use (warnings or higher) """
    logger.add(
        RichHandler(
            markup=True,  # Enables rich text formatting
            rich_tracebacks=True,  # Beautiful, colorized tracebacks
            show_time=True,
            show_level=True,
            show_path=True,
        ),
        level=LogType.WARNING.name,
        format="{message}",
        backtrace=False,
    )


def enable_debug_logging() -> None:
    """Enable debug output to stderr."""
    logger.remove()  # remove default handler
    logger.add(
        RichHandler(
            markup=True,  # Enables rich text formatting
            rich_tracebacks=True,  # Beautiful, colorized tracebacks
            show_time=True,
            show_level=True,
            show_path=True,
        ),
    )


def structured_sink(message) -> None:
    log_data = message.record["extra"].get("log_data")

    if log_data is not None:
        print(log_data)


def add_structured_log_sink(path: Path) -> None:
    """Add a structured log sink to the specified path."""
    logger.add(
        str(path),
        format="{extra[log_data]}",
        level=LogType.DEBUG.name,
        serialize=False,
        backtrace=True,
        diagnose=True,
        rotation=None,  # No rotation, since filename is already unique
        retention=None,
    )


def log_messages() -> None:
    """Log various messages at different severity levels."""
    logger.trace("A trace message.")
    logger.debug("A debug message.")
    logger.info("An info message.")
    logger.success("A success message.")
    logger.warning("A warning message.")
    logger.error("An error message.")
    logger.critical("A critical message.")


configure_logger()


def main() -> None:
    from contextlib import suppress

    """Main entry point of the application."""
    configure_logger()

    # Test cases
    LogType.WARNING.write("This is a clean warning message!")

    with suppress(TypeError):
        LogType.ERROR.raise_error(
            TypeError, "Uh Oh! This is not the right type!"
        )


if __name__ == "__main__":
    main()

# Signed off by Brian Sanford on 20260920
