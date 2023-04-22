# Written by: Justin Sadow "enshaeden"
# Contributing Editors:
# Date of last edit: 27 Jan, 2022
# Version: 1.0


from Primary import *
import Logger as log
import re


"""
Device specific functions that are not specific to any one device type
Functions are also not used by group or policy functions

@refined_device_details is used to gather the data from the device dict and return only the information needed to manage the device
@device_search is used to gather the data from the user and return the search parameter and search type
@group_search is used to gather the data from the groups dict and return the group id
"""


def refined_device_details(device_dict):
    # non-api function that refines the detials of a device to only the information needed to manage the device
    device_details = {
        'JSS_id': device_dict['general'].get('id', ''),
        'device_name': device_dict['general'].get('name', ''),
        'mac_address': device_dict['general'].get('mac_address', ''),
        'alt_mac_address': device_dict['general'].get('alt_mac_address', ''),
        'ip_address': device_dict['general'].get('ip_address', ''),
        'serial_number': device_dict['general'].get('serial_number', ''),
        'assigned_user': device_dict['location'].get('realname', ''),
        'username': device_dict['location'].get('username', ''),
        'user_email': device_dict['location'].get('email_address', ''),
    }
    return device_details


# @log.write_log    # uncomment this line to enable logging, currently logs entire device dict
def device_search(management_option, list_of_computers, list_of_noncomputers):
    """
    Jamf only effectively interacts with devices by name or serial number but other identifiers can be used to find those details
    If the user already knows the device name or serial number, they can use that to find the device
    If the user does not know the device name or serial number, they can use the other identifiers to find the device

    At the time of publication, the only other search integrated to the function is by IP_Address

    Parameters:
        question_known_device_name: Asks the user if they know the device serial
        search_type: contains the variable that identifies the search type to the calling function
        search_parameter: contains the variable that makes the device searchable based on search type
        list_of_devices: contains the list of devices returned from the API
        find_device: returns the device dict if the device is found

    Returns:
        search_type: contains the variable that identifies the search type to the calling function
        search_parameter: contains the variable that makes the device searchable based on search type
    """
    
    question_known_device = input(f"Do you know the serial number? (y/n)\n")
    
    if question_known_device == "y":
        search_type = "serial"
        search_parameter = input(f"What is the device serial number?\n=> ")
    
    elif question_known_device == "n":
        find_device = input(f"What is the name or ip address of the device?\n")
            # use regex matching to identify if the user is searching by name or ip address
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', find_device):
            search_type = "ip_address"
            search_parameter = ""
            try:
                if management_option == "computer":
                    list_of_devices = list_of_computers
                    management_option = "computers"
                elif management_option == "non-computer":
                    list_of_devices = list_of_noncomputers
                    management_option = "mobile_device"
                try:
                    for device in list_of_devices[management_option]:
                        if device['IP_Address'] == find_device:
                            search_type = "serial"
                            search_parameter = device['Serial_Number']
                            #TODO add date of last checkin verification
                            break
                except KeyError:
                    print("Error. No device found with that identifier.")           
            except:
                pass # error should be printed in above try blocks
        
        elif re.match(r'^[a-zA-Z0-9_.-]*$', find_device):
                # if the user is searching by name, output is just the name of the device
                search_type = "name"
                search_parameter = find_device
        else:
            print(f"Error. {find_device} is not a valid device name or ip address.")
            print("Exiting...")
    else:
        print(f"Input not valid. Please select either 'y' or 'n'")
    return search_parameter, search_type


# @log.write_log   # uncomment this line to enable logging, currently logs entire dict
def group_search(list_of_groups):
    """
    Asks the user if they know the group name or id
    If the user knows the group name or id, the function returns the group id
    If the user does not know the group name or id, the function asks the user for the group name and returns the group id

    Parameters:
        question_known_group: Asks the user if they know the group name or id
        group_id: contains the variable that makes the group searchable
        group_name: contains the variable that allows for searching the group id
        list_of_groups: contains the list of groups returned from the API
    
    Returns:
        group_id: contains the variable that makes the group searchable
    """
    
    question_known_group = input(f"Do you know the group id? (y/n)\n")
    if question_known_group == "y":
        group_id = input(f"What is the group id?\n=> ")
   
    elif question_known_group == "n":
        group_name = input(f"What is the group name?\n=> ")
        # get a list of all groups in jamf
        list_of_groups = list_of_groups
        # loop through the list of groups and find the group with the matching name
        # collect the group id
        try:
            for i in range(0, len(list_of_groups)):
                if group_name in list_of_groups[i]['name'] and list_of_groups[i]['is_smart'] == False:
                    group_id = list_of_groups[i]['id']
                    print(f"""
Group id: {group_id}
Group name: {list_of_groups[i]['name']}""")
        except KeyError:
            print("Error. No group found with that name.")
        except IndexError:
            print("Error. Index out of range.")
    
    else:
        print(f"Input not valid. Please select either 'y' or 'n'")
    
    return group_id
