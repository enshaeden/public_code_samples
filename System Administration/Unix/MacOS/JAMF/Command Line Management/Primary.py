# Written by: Justin Sadow "enshaeden"
# Contributing Editors: Matthew Warren "haircut", Alexander Bernier Siegler "aberniersiegler"
# Date of last edit: 27 Jan, 2022
# Version: 1.0


from datetime import datetime as dt
from authority import jssAuth
from ApiCommands import ObjectData
from ApiCommands import Computer
from ApiCommands import NonComputerDevice
from ApiCommands import groupMembership
import HTTPMethods as http
import startup_tasks as startup
import Logger as log
import os


"""
Primary operating script for the JAMF Command Line Management tool.
If run as the __main__ script, the following local functions will be run:

@clear: Clears the terminal
@management_selector: Allows the user to choose a managment option. It is wrapped in a logger module for auditing.

There are also a number of other functions that are called depending on the option selected in managment_selector.
Please review the documentation for each function to see what it does.

Parameters:
    None

Returns:
    None
"""


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


@log.write_log
def management_selector():
    """
    This function will display a list of management options and return the user's choice

    Parameters:
        management_option: The management option for the user to select
    
    Returns:
        management_option: The management option that was selected by the user
    """
    management_option = input("""
What would you like to manage?
    1. Computer
    2. Non-computer managed device
    3. Group membership
    4. Exit
=> """)
    if management_option == "1":
        management_option = "computer"
    elif management_option == "2":
        management_option = "noncomputer"
    elif management_option == "3":
        management_option = "group"
    elif management_option == "4":
        management_option = "exit"
    else:
        management_option = "invalid"
        print("Invalid selection. Please start over.")
        management_selector()
    return management_option


if __name__ == "__main__":
    # run startup checks and gather preliminary dictionary list data
    good_to_go, list_of_computers, list_of_groups, list_of_noncomputers = startup.main_checks()

    if good_to_go:
        clear()
        continue_managing = True
        while continue_managing:
            management_option = management_selector()

            if management_option == "computer" or management_option == "noncomputer":
                # get search parameter (name, serial, or ip_address) and qualify the search type (name, serial, ip_address)
                search_parameter, search_type = ObjectData.device_search(management_option, list_of_computers, list_of_noncomputers)
                if not search_parameter or not search_type:
                    clear()
                    print(f"\n\n\nDevice not found")
                    input("Press enter to exit and start over.")
                    continue_managing = False

                else:
                    if management_option == "computer":
                        search_addendum = "computer"
                        Computer.computer_manager(search_parameter, search_type, search_addendum)

                    if management_option == "noncomputer":
                        search_addendum = "noncomputer"
                        NonComputerDevice.noncomputer_manager(search_parameter, search_type, search_addendum)

            elif management_option == "group":
                groupMembership.manage_group_membership(list_of_groups, list_of_computers, list_of_noncomputers)

            elif management_option == "exit":
                print("Exiting script.")
                continue_managing = False