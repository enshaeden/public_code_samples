# Written by: Justin Sadow "enshaeden"
# Contributing Editors: Matthew Warren "haircut"
# Date of last edit: 27 Jan, 2022
# Version: 1.0


import os

from Primary import *
import HTTPMethods as http
import Logger as log


"""
Group specific functions that allow the user to add or remove a computer from a group and search for a group.

@clear: Clears the terminal
@manage_group_membership: Allows the user to add or remove a computer from a group and search for a group.
@get_list_of_groups: Returns a list of all groups as a JSON dict
@get_group_by_id: Returns a group by id as a JSON dict
@add_computer_to_group: Adds a computer to a group
@remove_computer_from_group: Removes a computer from a group
"""


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# @log.write_log   # Uncomment this line to write to log file, currently logs large dict
def manage_group_membership(list_of_groups, list_of_computers, list_of_noncomputers):
  """
  This function will allow the user to add or remove a computer from a group and search for a group.

  Parameters:
    device_type: Choose between computer or noncomputer managed device
    group_id: Calls a function to search for a group by id
    device_search_type: Attribute that holds name, serial, or ip_address
    device_search: Calls a function to search for a computer or noncomputer managed device
    search_addendum: Attribute that tells a called function what menu to show, contextually
    add_or_remove: Prompt to add or remove a computer from a group
    add_code: Calls a function to add a computer to a group
    remove_code: Calls a function to remove a computer from a group

  Returns:
    None
  """
  clear()
  device_type = input(f"""
What type of device would you like to manage?
    1. Computer
    2. Non-computer device
    3. Exit
=> """)
  group_id = ObjectData.group_search(list_of_groups)
    # devices are added to the group by device id
  
  if device_type == "1":
        device_type = "computer"
        device_search, device_search_type = ObjectData.device_search(device_type, list_of_computers, {})
        search_addendum = "group"
        device_details = Computer.computer_manager(device_search, device_search_type, search_addendum)
  elif device_type == "2":
        device_type = "noncomputer"
        device_search, device_search_type = ObjectData.device_search(device_type, {}, list_of_noncomputers)
        search_addendum = "group"
        device_details = NonComputerDevice.noncomputer_manager(device_search, device_search_type, search_addendum)
  
  if device_details != "" and group_id != "":
    add_or_remove = input(f"""
Would you like to (a)dd or (r)emove {device_details['device_name']} from {group_id}?
""").lower()
    if add_or_remove == "a":
      try:
        add_code = add_device_to_group(device_details, group_id, device_type)
        if add_code >= 200 and add_code <= 299:
            print(f"{device_details['device_name']} has been added to {group_id}.")
            input("Press enter to return to the main menu.")
      except:
            print(f"{device_details['device_name']} could not be added to group {group_id}. Error: {add_code}")
    
    elif add_or_remove == "r":
        try:
          remove_code = remove_device_from_group(device_details, group_id, device_type)
          if remove_code >= 200 and remove_code <= 299:
              print(f"{device_details['device_name']} has been removed from {group_id}.")
              input("Press enter to return to the main menu.")
        except:
            print(f"{device_details['device_name']} could not be removed from group {group_id}. Error: {remove_code}")
  return


@log.write_log
def get_list_of_groups():
    # the endpoint for the group list is actually a saved search
    # the search name and data is "All Groups"
    endpoint = f"/computergroups"
    groups_response = http.make_get_request(endpoint)
    # This is going to return a JSON dict
    # We expect there to be a 'computer_group' key
    # if there is not, return empty Dict
    return groups_response.get('computer_groups', {})

@log.write_log
def get_list_of_noncomputer_groups():
  endpoint = f"/mobiledevicegroups"
  groups_response = http.make_get_request(endpoint)
  return groups_response.get('mobile_device_group', {})


@log.write_log
def get_group_by_id(group_id, device_type):
  if device_type == "computer":
    # this endpoint is a computer group by group id
    endpoint = f"/computergroups/id/{group_id}"
  elif device_type == "noncomputer":
    endpoint = f"/mobiledevicegroups/id/{group_id}"
  groups_response = http.make_get_request(endpoint)
  # We expect there to be a computers key
  # if there is not, return empty Dict
  return groups_response.get('computers', {})


@log.write_log
def add_device_to_group(device_details, group_id, device_type):
    # this endpoint is a computer group by group id
    # this function is only effective if you know the exact device id and group id
  if device_type == "computer":
    endpoint = f"/computergroups/id/{group_id}"
    xml = f"""<computer_group>
  <computer_additions>
    <computer>
      <id>{device_details['JSS_id']}</id>
      <serial_number>{device_details['serial_number']}</serial_number>
    </computer>
  </computer_additions>
</computer_group>"""
  elif device_type == "noncomputer":
    endpoint = f"/mobiledevicegroups/id/{group_id}"
    xml = f"""<mobile_device_group>
    <mobile_device_additions>
        <mobile_device>
            <id>{device_details['JSS_id']}</id>
            <serial_number>{device_details['serial_number']}</serial_number>
        </mobile_device>
    </mobile_device_additions>
</mobile_device_group>"""
  groups_response = http.make_put_request(endpoint, xml)
  return groups_response


@log.write_log
def remove_device_from_group(device_details, group_id, device_type):
    # this endpoint is a computer group by group id
    # this function is only effective if you know the exact device id and group id
  if device_type == "computer":  
    endpoint = f"/computergroups/id/{group_id}"
    body = f"""
<computer_group>
  <computer_deletions>
    <computer>
      <id>{device_details['JSS_id']}</id>
      <serial_number>{device_details['serial_number']}</serial_number>
    </computer>
  </computer_deletions>
</computer_group>"""
  elif device_type == "noncomputer":
    endpoint = f"/mobiledevicegroups/id/{group_id}"
    xml = f"""<mobile_device_group>
    <mobile_device_deletions>
        <mobile_device>
            <id>{device_details['JSS_id']}</id>
            <serial_number>{device_details['serial_number']}</serial_number>
        </mobile_device>
    </mobile_device_deletions>
</mobile_device_group>"""
  groups_response = http.make_put_request(endpoint, body)
  return groups_response
