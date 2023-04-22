# Written by: Justin Sadow "enshaeden"
# Contributing Editors:
# Date of last edit: 3 Feb, 2022
# Version: 1.0


from time import sleep
import os
from pprint import pprint as pp
from Primary import *
import HTTPMethods as http
import Logger as log


"""
Functions specific to the management of noncomputer devices in Jamf

@clear: Clears the terminal
@noncomputer_manager: Allows the user to choose a managment option. It is wrapped in a logger module for auditing.
@get_noncomputer_device_list: Returns a list of all noncomputer devices as a JSON dict
@get_noncomputer_device_by_name: Returns a noncomputer device by name as a JSON dict
@get_noncomputer_device_by_serial_number: Returns a noncomputer device by serial number as a JSON dict
@lock_noncomputer_device: Locks a noncomputer device by device id
"""


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


@log.write_log
def noncomputer_manager(search_parameter, search_type, search_addendum):
    """
    Function to allow the user to choose what options they would like to manage noncomputer devices with.

    Parameters:
        device_details: Dict containing the noncomputer device details, default is empty dict
        exception_occured: Boolean to indicate if an exception has occured, default is False
        menu_skip: Boolean to indicate if the user has selected an option that allows the user to skip the menu, default is False
        search_parameter: The device search parameter (name, serial)
        search_type: The device search type (name, serial)
        search_addendum: The device search addendum (group search or device search)
        management_option: The device management option of either Lock or Erase
        be_absolutly_sure: The user's confirmation of the management option
        affirmation: The user's confirmation of the management option
        device_lock: endpoint status code for lock command
        passcode: The generated passcode for the lock command

    Returns:
        device_details: A JSON dict of the noncomputer device details
    """
    device_details = {}
    exception_occured = False
    menu_skip = False
    try:
        if search_type == "name":
            device_dict = get_noncomputer_by_name(search_parameter)
        if search_type == "serial":
            device_dict = get_noncomputer_by_serial_number(search_parameter)
    except:
        exception_occured = True
        print(f"An error has occured while attempting to retrieve the device details for {search_parameter}")
        sleep(1)
    if not device_details and not exception_occured:
        device_details = ObjectData.refined_device_details(device_dict)
    clear()
    if search_addendum == "noncomputer" and not exception_occured:
        management_option = input(f"""
Device Details:

User: {device_details['assigned_user']}
Device Name: {device_details['device_name']}
Serial Number: {device_details['serial_number']}
Mac Address: {device_details['mac_address']}

    Options:
    1. Lock
    2. Change group membership
    3. Display details
    4. Return to main menu
=> """)

        if management_option == "1":
            be_absolutely_sure = input("Are you sure you want to lock this device? (y/n)\n=> ").lower()
            if be_absolutely_sure == "y":
                affirmation = input(f"""
********************************************************************
                                                            
Are you ABSOLUTELY certain you want to lock {device_details['device_name']}?
                                                                
********************************************************************

This action will prevent the user from working until they contact the Help Desk.

Enter "I agree" to continue or "n" to go back.
""").lower()
                
                if affirmation == "i agree":
                    try:
                        lock_response = lock_noncomputer(device_details['id'])
                        if lock_response.status_code >= 200 and lock_response.status_code <= 299:
                            print(f"{device_details['device_name']} has been locked.")
                            input("Press enter to return to the main menu.")
                    except:
                        print(f"{device_details['device_name']} could not be locked. Error: {lock_response}")
                        input("Press enter to return to the main menu.")
                        exception_occured = True
                
                elif affirmation == "n":
                    print("Returning to menu.")
        
        elif management_option == "2":
            search_addendum = "group"
            menu_skip = True
        
        elif management_option == "3":
            print(f"{device_details['device_name']}'s details:")
            pp(device_details)
            input("Press enter to return to the main menu.")
        
        elif management_option == "4":
            input(f"\nPress return to main menu\n")
    
    elif search_addendum == "group" and not exception_occured:
        if menu_skip:
            return device_details
        else:
            management_option = input("""
    Options:
    1. Device Details
    2. Cancel
=> """)
        
        if management_option == "1":
            print(f"{device_details['device_name']}'s device details:")
            pp(device_details)
            input("Press enter to return to group options.")
            return device_details
        
        elif management_option == "2":
            device_details = ""
            return device_details
    elif exception_occured:
        input("Press enter to return to the main menu.")
        
    return


@log.write_log
def get_noncomputer_device_list():
    endpoint = "/mobiledevices"
    device_list = http.make_get_request(endpoint)
    # This is going to return a JSON dict
    # one of the keys will be mobile_devices
    # We expect there to be a mobile_devices key
    # if there is not, return empty Dict
    return device_list.get('mobile_devices', {})


@log.write_log
def get_noncomputer_by_serial_number(serial_number):
    endpoint = f"/mobiledevices/serialnumber/{serial_number}"
    groups_response = http.make_get_request(endpoint)
    # We expect there to be a restricted_software key
    # if there is not, return empty Dict
    return groups_response.get('mobile_devices', {})


@log.write_log
def get_noncomputer_by_name(name):
    endpoint = f"/mobiledevices/name/{name}"
    groups_response = http.make_get_request(endpoint)
    # We expect there to be a restricted_software key
    # if there is not, return empty Dict
    return groups_response.get('mobile_device', {})


@log.write_log
def lock_noncomputer(device_id):
    lock_message = "This device has been reported lost or stolen. If you need assistance, please reach out to it-911@lyft.com."
    endpoint = f"/mobiledevicecommands/command/DeviceLock/{lock_message}/id/{device_id}"
    lock_response = http.make_post_request(endpoint)
    return lock_response