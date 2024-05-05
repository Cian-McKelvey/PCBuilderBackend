import logging
import os


def create_logger(filename: str):
    """
    Creates a logger instance with specified filename and sets up logging handlers.

    :param filename: Name of the log file.
    :return: Logger instance.
    """
    # Get the absolute path to the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    log_file_path = os.path.join(project_root, 'logs', filename)

    # Create a new logger instance with a unique name
    logger_instance = logging.getLogger(f"logger_{filename}")

    # Sets the lowest level of logger to the debug level (lowest)
    logger_instance.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a console handler and set the formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Create a file handler and set the formatter
    file_handler = logging.FileHandler(filename=log_file_path)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger_instance.addHandler(console_handler)
    logger_instance.addHandler(file_handler)

    return logger_instance
