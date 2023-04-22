# Author: Justin Sadow "enshaeden"
# Date of last edit: 25 Jan, 2022
# Version: 1.0


import time
import os
from Primary import *
import Logger as log


"""
This module contains functions for starting the JAMF Command Line Management tool and checking service availability

@clear: Clears the terminal
@timer: Decorator to time the execution of a function
@connection_test: Tests the connection to the JSS
@get_computer_list: Returns all computers as a JSON dict
@get_list_of_groups: Returns a list of all groups as a JSON dict
@main_checks: Calls all of the previous functions to verify the program may continue
"""


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"\n{func.__name__} started...")
        func(*args, **kwargs)
        end = time.time()
        time_elapsed = round(end - start)
        print(f"{func.__name__} completed in {time_elapsed} seconds")
        val = func(*args, **kwargs)
        return val
    return wrapper


@log.write_log
def connection_test():
    """
    This function will check if the connection to the management server is working.

    Parameters:
        connection_healthy: Boolean value that will be returned to the calling function
        connection_health: Function call to check the connection to the management server

    Returns:
        connection_healthy: Boolean value that will be returned to the calling function. False will terminate the program
    """
    connection_healthy = False
    connection_health = http.test_jamf_connection()
    if connection_health:
       connection_healthy = True
    return connection_healthy


@timer
def get_computer_list():
    """
    This function will get a list of all computers in the JSS.

    Parameters:
        computer_list: Makes a function call to the JSS to get a list of all computers
    
    Returns:
        computer_list: List of all computers in the JSS as a dict
    """
    list_of_computers = Computer.get_list_of_computers()
    if not list_of_computers:
        assert False; print(f"Could not retrieve computer list")
    return list_of_computers


@timer
def get_list_of_groups():
    """
    This function will get a list of all groups in the JSS.

    Parameters:
        list_of_groups: Makes a function call to the JSS to get a list of all groups

    Returns:
        list_of_groups: List of all groups in the JSS as a list of dicts
    """
    list_of_groups = groupMembership.get_list_of_groups()
    if not list_of_groups:
        assert False; print(f"Could not retrieve list of groups")
    return list_of_groups


@timer
def get_list_of_noncomputers():
    """
    This function will get a list of all non-computers in the JSS.

    Parameters:
        list_of_noncomputers: Makes a function call to the JSS to get a list of all non-computers

    Returns:
        list_of_noncomputers: List of all non-computers in the JSS as a list of dicts
    """
    list_of_noncomputers = NonComputerDevice.get_noncomputer_device_list()
    if not list_of_noncomputers:
        assert False; print(f"Could not retrieve list of non-computer devices")
    return list_of_noncomputers


@log.write_log
def main_checks():
    """
    The main checks function will run all the checks to make sure the program can run.

    Parameters:
        good_to_go: Boolean value that will be returned to the calling function

    Returns:
        good_to_go: Boolean value that will be returned to the calling function. False will terminate the program
        list_of_computers: List of all computers in the JSS as a dict
        list_of_groups: List of all groups in the JSS as a list of dicts
    """
    clear()
    good_to_go = False
    print(f"Starting initial checks...\n")
    connection_healthy = connection_test()
    if connection_healthy:
        list_of_computers = get_computer_list()
        list_of_groups = get_list_of_groups()
        list_of_noncomputers = get_list_of_noncomputers()
        good_to_go = True
        print(f"All checks passed.")
        time.sleep(1)
    else:
        assert False, print(f"Could not connect to JAMF server")
    return good_to_go, list_of_computers, list_of_groups, list_of_noncomputers