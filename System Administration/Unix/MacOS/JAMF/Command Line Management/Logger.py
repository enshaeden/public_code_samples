from datetime import datetime as dt
import os


def write_log(function):
    """
    This function will write to a log file
    """
    def wrapper(*args, **kwargs):
        with open("jamf_management_log.txt", "a") as log:
            log.write(f"""
            User: {os.getlogin()}
            Time: {dt.now()}
            Function: {function.__name__}
                Input Arguments: {args}
                Keyword Arguments: {kwargs}
            """)
        val = function(*args, **kwargs)
        return val
    return wrapper
