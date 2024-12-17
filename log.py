import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FORMAT = "%(asctime)s %(levelname)s %(lineno)d - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = "logs/app.log"
LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10 MB

def setup_logging(log_to_console=False):
    """
    Configure logging settings for the application.
    
    :param log_to_console: If True, also log to console. If False, log only to file.
    """
    # Remove any existing handlers to prevent duplicate logging
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # Create the log directory if it doesn't exist
    log_dir = os.path.dirname(LOG_FILE)
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating log directory: {e}")
            return
    
    # Set up the rotating file handler
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=LOG_FILE_MAX_SIZE, backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(file_handler)
    
    # Optionally add console handler
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
        logger.addHandler(console_handler)
        
    return logger