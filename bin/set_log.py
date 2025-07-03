
from bin.get_packages import * 
import sys
import logging


try:
    handler_info = logging.FileHandler(PATH_LOG_FILE, mode="a", encoding="utf-8")
    # handler_error = logging.FileHandler(PATH_OUTPUT + "/log/error.log", mode="a", encoding="utf-8")
    # handler_warning = logging.FileHandler(PATH_OUTPUT + "/log/warning.log", mode="a", encoding="utf-8")

    formatter = logging.Formatter("%(asctime)-10s:%(levelname)-20s:%(name)s:%(message)-20s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler_info.setFormatter(formatter)
    handler_info.setLevel(logging.INFO)
    logger.addHandler(handler_info)

    # handler_error.setFormatter(formatter)
    # handler_error.setLevel(logging.ERROR)
    # logger.addHandler(handler_error)

    # handler_warning.setFormatter(formatter)
    # handler_warning.setLevel(logging.WARNING)
    # logger.addHandler(handler_warning)

except FileNotFoundError:
    open(PATH_LOG+"/info.log", 'a').close()

    open(PATH_OUTPUT+"/log/warning.log", 'a').close()

    open(PATH_OUTPUT+"/log/error.log", 'a').close()

 