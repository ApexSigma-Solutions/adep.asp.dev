"""Logging configuration for the ApexSigma ecosystem."""

import logging

def get_logger(name: str) -> logging.Logger:
    """Configures and returns a logger.

    Args:
        name: The name of the logger, typically __name__.

    Returns:
        A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
