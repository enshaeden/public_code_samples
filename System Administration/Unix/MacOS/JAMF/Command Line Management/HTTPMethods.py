# Justin Sadow
# Version: 1.0

from Primary import *
import requests
from Logger import write_log


@write_log
def test_jamf_connection():
    """
    This function will test the connection to the JAMF server by making a GET request to the JSS for a list of computers
    Success is determined as a length of the returned list of computers > 1

    @return: True if the connection is successful, False if not
    """
    endpoint = "/computers"
    test_response = make_get_request(endpoint)
    # This will return a decoded JSON dict
    # one of the keys will be 'computers'
    computers = test_response['computers']
    connection_health = False
    if len(computers) < 1:
        Exception("JAMF Isn't Working")
    else:
        print(f"JAMF connection is healthy")
        connection_health = True
    return connection_health


@write_log
def make_get_request(endpoint):
    # Load JAMF Credentials
    username = jssAuth.username
    password = jssAuth.password
    # Log into JAMF and make sure its working
    base = "https://gozer.lyft-corp.net:8443/JSSResource"
    # Concatinate endpoint and base URL
    url = f"{base}{endpoint}"
    # Change the HTTPD header to be application/json
    my_headers = {'Accept': 'application/json'}
    # Python Requests will want Basic Auth as a username/password tuple
    resp = requests.get(url, headers=my_headers, auth=(username,password))
    return resp.json()

@write_log
def make_put_request(endpoint, body):
    # Load JAMF Credentials
    username = jssAuth.username
    password = jssAuth.password
    # Log into JAMF and make sure its working
    base = "https://gozer.lyft-corp.net:8443/JSSResource"
    # Concatinate endpoint and base URL
    url = f"{base}{endpoint}"
    # Change the HTTPD header to be application/xml
    my_headers = {
        'Accept': 'application/xml',
        'content-type': 'application/xml'
    }
    # Python Requests will want Basic Auth as a username/password tuple
    resp = requests.put(
        url,
        headers=my_headers,
        data=body,
        auth=(username,password)
    )
    return resp.status_code

@write_log
def make_post_request(endpoint, body):
    # Load JAMF Credentials
    username = jssAuth.username
    password = jssAuth.password
    # Log into JAMF and make sure its working
    base = "https://gozer.lyft-corp.net:8443/JSSResource"
    # Concatinate endpoint and base URL
    url = f"{base}{endpoint}"
    # Change the HTTPD header to be application/xml
    my_headers = {
        'Accept': 'application/xml',
        'content-type': 'application/xml'
    }
    # Python Requests will want Basic Auth as a username/password tuple
    resp = requests.post(
        url,
        headers=my_headers,
        data=body,
        auth=(username,password)
    )
    return resp.status_code

@write_log
def make_delete_request(endpoint):
    # Load JAMF Credentials
    username = jssAuth.username
    password = jssAuth.password
    # Log into JAMF and make sure its working
    base = "https://gozer.lyft-corp.net:8443/JSSResource"
    # Concatinate endpoint and base URL
    url = f"{base}{endpoint}"
    # Change the HTTPD header to be application/xml
    my_headers = {
        'Accept': 'application/xml',
        'content-type': 'application/xml'
    }
    # Python Requests will want Basic Auth as a username/password tuple
    resp = requests.delete(
        url,
        headers=my_headers,
        auth=(username,password)
    )
    return resp.status_code
