import logging
import sys

logger = logging.getLogger(__name__)


def configure_logger(logger: logging.Logger, verbosity: int):
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    # Default logger level is logging.WARNING
    logger.setLevel(logging.WARNING - min(verbosity, 2) * 10)