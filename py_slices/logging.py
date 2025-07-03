import logging
import traceback
import os

def setup_logger(logfile="publish_log.txt", developer_logfile="DevMode.log", mode="Brief", enable_logging=True):
    logger = logging.getLogger("cyberpublisher")
    logger.handlers.clear()  # Remove all handlers to avoid duplicates
    logger.propagate = False  # Prevent double logging

    if not enable_logging:
        logger.disabled = True
        return logger

    # For Brief mode, remove the log file at the start of each run to avoid mixed formats
    if mode == "Brief" and os.path.exists(logfile):
        os.remove(logfile)

    logger.setLevel(logging.DEBUG if mode == "DevMode" else logging.INFO)
    # Use simple formatter for Brief mode, detailed for others
    if mode == "Brief":
        formatter = logging.Formatter('%(message)s')
    else:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    if mode == "DevMode":
        dev_fh = logging.FileHandler(developer_logfile)
        dev_fh.setLevel(logging.DEBUG)
        dev_fh.setFormatter(formatter)
        logger.addHandler(dev_fh)
    else:
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.INFO if mode == "Brief" else logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    logger.disabled = False
    return logger

def log_event(logger, message, level="info", mode="Brief", enable_logging=True):
    if not enable_logging:
        return
    if mode == "Brief" and level != "info":
        return  # Only log info in Brief mode
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "debug" and mode in ["Verbose", "DevMode"]:
        logger.debug(message)

def log_exception(logger, exc, mode="Brief", enable_logging=True):
    if not enable_logging:
        return
    logger.error("Exception occurred", exc_info=exc)
    if mode == "DevMode":
        with open("DevMode.log", "a") as devlog:
            devlog.write("\n=== Exception Caught ===\n")
            devlog.write(traceback.format_exc())
            devlog.write("\n")
