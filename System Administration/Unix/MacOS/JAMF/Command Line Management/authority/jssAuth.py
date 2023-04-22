from os import environ as keyring


"""
This module is designed to allow the user to choose their credentialing method for accessing the JSS server.
Username and password variables can be set in this script or stored as an environment variable.

If the function does not detect a username or password, it will prompt the user for input.
"""


def get_credentials():
    username = ""
    password = ""
    if username == "" or password == "":
        username = keyring.get('JSS_USER')
        password = keyring.get('JSS_PASS')
        if username == None or password == None:
            username = input("Enter your JSS username: ")
            password = input("Enter your JSS password: ")
    return username, password


username, password = get_credentials()