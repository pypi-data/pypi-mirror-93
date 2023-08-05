import requests
from zephyr_sdk.exceptions.ZExceptions import ZAPIError
from zephyr_sdk.exceptions.ZExceptions import MissingParametersError


# Create a release with the information passed in
def create_release(client, release_spec):
    url = client.base_url + '/release/'
    headers = {
        'Authorization': 'Bearer ' + client.token,
        'Content-Type': 'application/json'
    }

    # Validate the release_spec variable
    error_list = []
    if 'name' not in release_spec:
        error_list.append("name")

    if 'releaseStartDate' not in release_spec:
        error_list.append("releaseStartDate")

    if 'releaseEndDate' not in release_spec:
        error_list.append("releaseEndDate")

    if 'projectId' not in release_spec:
        error_list.append("projectId")

    # If any errors were added to the list, raise an exception
    if len(error_list) > 0:
        raise MissingParametersError(error_list)

    # Otherwise make the API call.
    r = requests.post(url, json=release_spec, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()


# Delete a release by release id.
def delete_release(client, release_id):
    url = client.base_url + '/release/' + str(release_id)
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.delete(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()


# Get details of a release by the release id
def get_release_by_release_id(client, release_id):
    url = client.base_url + '/release/' + str(release_id)
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()


# Get all releases for a project
def get_releases_for_a_project(client, project_id):
    url = client.base_url + '/release/project/' + str(project_id)
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()


# Create a release with the information passed in
def update_release(client, release_id, release_spec):
    # Get info on the release to fill the request.
    release_info = client.get_release_by_release_id(release_id)

    url = client.base_url + '/release/' + str(release_id)
    headers = {
        'Authorization': 'Bearer ' + client.token,
        'Content-Type': 'application/json'
    }

    # Go through the request info, and replace any values in there with values
    # from release spec.
    for key, value in release_info.items():
        if key not in release_spec:
            release_spec[key] = value

    # Otherwise make the API call.
    r = requests.put(url, json=release_spec, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()
