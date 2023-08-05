import requests
from zephyr_sdk.exceptions.ZExceptions import ZAPIError
from zephyr_sdk.exceptions.ZExceptions import MissingParametersError


# Create an execution cycle
def create_cycle(client, cycle_spec):
    url = client.base_url + '/cycle'
    headers = {
        "Authorization": "Bearer " + client.token,
        "Content-Type": "application/json"
    }

    # Validate the request body
    error_list = []

    # Check for the required parameters
    required_parameters = [
        'name',
        'releaseId',
        'cycleStartDate',
        'cycleEndDate'
    ]
    for parameter in required_parameters:
        if parameter not in cycle_spec:
            error_list.append(parameter)

    if len(error_list) > 0:
        raise MissingParametersError(error_list)

    r = requests.post(url, headers=headers, json=cycle_spec)

    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()


# Delete an execution cycle
def delete_cycle(client, cycle_id):
    url = client.base_url + '/cycle/' + str(cycle_id)
    headers = {
        "Authorization": "Bearer " + client.token
    }

    r = requests.delete(url, headers=headers)

    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()


# Get execution cycle by cycle id.
def get_cycle_by_id(client, cycle_id):
    url = client.base_url + '/cycle/' + str(cycle_id)
    headers = {
        "Authorization": "Bearer " + client.token
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()


# Get execution cycles in a release.
def get_cycles_for_release(client, release_id):
    url = client.base_url + '/cycle/release/' + str(release_id)
    headers = {
        "Authorization": "Bearer " + client.token
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()


# Create an execution cycle
def update_cycle(client, cycle_id, cycle_spec):
    url = client.base_url + '/cycle/' + str(cycle_id)
    headers = {
        "Authorization": "Bearer " + client.token,
        "Content-Type": "application/json"
    }

    cycle_info = client.get_cycle_by_id(cycle_id)

    for parameter in cycle_info:
        if parameter not in cycle_spec:
            cycle_spec[parameter] = cycle_info[parameter]

    r = requests.put(url, headers=headers, json=cycle_spec)

    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()
