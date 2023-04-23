import logging


def configure_logging(verbose=True):
    # For everybody else, log at INFO level
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    # For this application, log at DEBUG level. May be adjusted if too verbose.
    logger = logging.getLogger("uploader")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
