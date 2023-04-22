# Written by: Justin Sadow "enshaeden"
# Contributing Editors:
# Date of last edit: 27 Jan, 2022
# Version: 1.0


import os
from pprint import pprint as pp
from time import sleep
from Primary import *
import HTTPMethods as http
import Logger as log
import random


"""
Computer specific functions that allow the user to lock or erase a computer or gather device details.

@clear: Clears the terminal
@computer_manager: Allows the user to choose a managment option. It is wrapped in a logger module for auditing.
@get_list_of_computers: Returns a list of all computers as a JSON dict
@get_computer_by_name: Returns a computer by name as a JSON dict
@get_computer_by_serial_number: Returns a computer by serial number as a JSON dict
@lock_computer: Locks a computer by computer id
@erase_computer: Erases a computer by computer id
"""


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


@log.write_log
def computer_manager(search_parameter, search_type, search_addendum):
    """ 
    This function will initiate the computer management process.
    There are two branches of the function:
        1. If the user initiated a search by computer the user will be presented with computer management options
        2. If the user initiated a search by way of group management the user will only be presented with device detail options

    Parameters:
        search_parameter: The device search parameter
        search_type: The device search type
        management_option: The device management option of either Lock or Erase
        be_absolutly_sure: The user's confirmation of the management option
        affirmation: The user's confirmation of the management option
        device_lock: endpoint status code for lock command
        passcode: The generated passcode for the lock command
    
    Returns:
        computer_details: A JSON dict of the computer details
    """
    computer_details = {}
    exception_occured = False
    try:
        if search_type == "name":
            device_dict = get_computer_by_name(search_parameter)
        if search_type == "serial":
            device_dict = get_computer_by_serial_number(search_parameter)
    except:
        print(f"An error has occured while attempting to retrieve the device details for {search_parameter}")
        exception_occured = True
        sleep(1)
    
    if not computer_details and not exception_occured:
            computer_details = ObjectData.refined_device_details(device_dict)
    
    clear()
    
    if search_addendum == "computer" and not exception_occured:
        management_option = input(f"""
Computer Details:

User: {computer_details['assigned_user']}
Device Name: {computer_details['device_name']}
Serial Number: {computer_details['serial_number']}
Mac Address: {computer_details['mac_address']}

    Options:
    1. Lock
    2. Erase
    3. Device Details
    4. Return to main menu
=> """)
        
        if management_option == "1":
            be_absolutely_sure = input("Are you sure you want to lock this computer? (y/n)\n=> ").lower()
            if be_absolutely_sure == "y":
                affirmation = input(f"""
********************************************************************
                                                            
Are you ABSOLUTELY certain you want to lock {computer_details['device_name']}?
                                                                
********************************************************************

This action will prevent the user from working until they contact the Help Desk.

Enter "I agree" to continue or "n" to go back.
""").lower()
                
                if affirmation == "i agree":
                    try:
                        device_lock, passcode = lock_computer(computer_details['JSS_id'])
                        if device_lock.status_code >= 200 and device_lock.status_code <= 299:
                            print(f"{computer_details['device_name']} has been locked with passcode {passcode}.")
                            input("Press enter to return to the main menu.")
                    except:
                        print(f"{computer_details['device_name']} could not be locked. Error: {device_lock.status_code}")
                        exception_occured = True
                
                elif affirmation == "n":
                    print("Returning to menu.")

        elif management_option == "2":
            be_absolutely_sure = input("Are you sure you want to erase this computer? (y/n)\n=> ")
            if be_absolutely_sure == "y":
                affirmation = input(f"""
********************************************************************
                                                            
Are you ABSOLUTELY certain you want to erase {computer_details['device_name']}?
                                                                
********************************************************************

This action will permanently erase any information on the computer unless there is a backup.

Enter "I agree" to continue or "n" to go back.
""")
                
                if affirmation == "I agree":
                    try:
                        device_erase = erase_computer(computer_details['JSS_id'])
                        if device_erase.status_code >= 200 and device_erase.status_code <= 299:
                            print(f"{computer_details['device_name']} has been erased.")
                            input("Press enter to return to the main menu.")
                    except:
                        print(f"{computer_details['device_name']} could not be erased. Error: {device_erase.status_code}")
                        exception_occured = True
                
                elif affirmation == "n":
                    print("Returning to menu.")
        
        elif management_option == "3":
            print(f"{computer_details['device_name']}'s device details:")
            pp(computer_details)
            input("Press enter to return to the main menu.")
            return computer_details
        
        elif management_option == "4":
            print("Returning to main menu.")
    
    if search_addendum == "group" and not exception_occured:
        management_option = input("""
    Options:
    1. Device Details
    2. Cancel
=> """)
        
        if management_option == "1":
            print(f"{computer_details['device_name']}'s device details:")
            pp(computer_details)
            input("Press enter to return to group options.")
            return computer_details
        
        elif management_option == "2":
            computer_details = ""
            return computer_details
    
    elif exception_occured:
        input("Press enter to return to the main menu.")
    
    return


@log.write_log
def get_list_of_computers():
    # the endpoint for the computer list is actually a saved search
    # the search name and data is "All Computers"
    endpoint = "/advancedcomputersearches/id/107"
    device_list = http.make_get_request(endpoint)
    # This is going to return a JSON dict
    # We expect there to be a 'advanced_computer_search' key
    # if there is not, return empty Dict
    return device_list.get('advanced_computer_search', {})


@log.write_log
def get_computer_by_name(name):
    # this endpoint is a computer by name
    # this search is only effective if you know the exact device name and there are no duplicates
    endpoint = f"/computers/name/{name}"
    groups_response = http.make_get_request(endpoint)
    # We expect there to be a computer key
    # if there is not, return empty Dict
    return groups_response.get('computer', {})     # potential error, may be 'general'


@log.write_log
def get_computer_by_serial_number(serial_number):
    # this endpoint is a computer by serial number
    # this search is only effective if you know the exact device name and there are no duplicates
    endpoint = f"/computers/serialnumber/{serial_number}"
    groups_response = http.make_get_request(endpoint)
    # We expect there to be a computer key
    # if there is not, return empty Dict
    return groups_response.get('computer', {})     # potential error, may be 'general'


@log.write_log
def lock_computer(computer_id):
    # generates a passcode and locks the computer
    passcode_list = []
    for i in range(0, 6):
        passcode_list.append(random.randint(0, 9))
    passcode = ''.join(str(x) for x in passcode_list)
    endpoint = f"/computercommands/command/DeviceLock/passcode/{passcode}/id/{computer_id}"
    device_lock = http.make_post_request(endpoint)
    return device_lock, passcode


@log.write_log
def erase_computer(computer_id):
    # generates a passcode and erases the computer
    passcode_list = []
    for i in range(0, 6):
        passcode_list.append(random.randint(0, 9))
    passcode = ''.join(str(x) for x in passcode_list)
    endpoint = f"/computercommands/command/EraceDevice/passcode/{passcode}/id/{computer_id}"
    device_erase = http.make_post_request(endpoint)
    return device_erase, passcode