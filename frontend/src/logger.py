import logging

def get_logger(name):
    """
    Returns a logger with the specified name.
    """

    # Logging Configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(name)
