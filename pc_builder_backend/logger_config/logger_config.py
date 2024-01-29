import logging
import os


def create_logger(filename: str):
    # Get the absolute path to the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    log_file_path = os.path.join(project_root, 'logs', filename)

    logger = logging.getLogger(__name__)

    # Sets the lowest level of logger to the debug level (lowest)
    logger.setLevel(logging.DEBUG)  # This will need to be changed in the real app
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Create a console handler and set the formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # Sets the logging to write to app.log too
    file_handler = logging.FileHandler(filename=log_file_path)
    file_handler.setFormatter(formatter)  # Sets the format
    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
