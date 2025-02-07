import logging
from logging.handlers import RotatingFileHandler


def get_logger(name: str, log_file: str = "app.log", level: int = logging.INFO) -> logging.Logger:
    """
    Creates and returns a logger instance with both console and file handlers.

    Args:
        name (str): The name of the logger (usually the __name__ of the module).
        log_file (str): The file where logs will be saved. Defaults to 'app.log'.
        level (int): The logging level (e.g., logging.DEBUG, logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a logger instance
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate logs if the logger is reused
    if logger.hasHandlers():
        return logger

    # Formatter for log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # File handler with rotation (10MB per file, keep 3 backups)
    file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
