import logging
import sys


def setup_logging(config=None):

    log_level = "INFO"
    if config:
        log_level = config.data.get("log_level", "INFO").upper()

    if log_level == "OFF":
        logging.disable(logging.CRITICAL)
        return logging.getLogger()

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    console.setFormatter(fmt)
    root_logger.addHandler(console)

    file_handler = logging.FileHandler(config.data["log_file"], encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    root_logger.addHandler(file_handler)

    return root_logger
