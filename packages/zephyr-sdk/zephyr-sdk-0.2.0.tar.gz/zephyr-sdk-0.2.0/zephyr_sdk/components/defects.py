import requests
from zephyr_sdk.exceptions.ZExceptions import ZAPIError
from zephyr_sdk.exceptions.ZExceptions import MissingParametersError
from zephyr_sdk.exceptions.ZExceptions import ResourceNotFoundError


def create_defect(client, defect_spec):
    url = client.base_url + '/defect'
    headers = {
        "Authorization": "Bearer " + client.token,
        "Content-Type": "application/json"
    }

    # Validate the request body
    error_list = []

    # Check for the required parameters
    required_parameters = [
        'projectId',
        'product',
        'target_milestone',
        'hardware',
        'longDesc',
        'status',
        'version',
        'severity',
        'assigned_to',
        'component',
        'shortDesc',
        'op_sys',
        'priority'
    ]
    for parameter in required_parameters:
        if parameter not in defect_spec:
            error_list.append(parameter)

    if len(error_list) > 0:
        raise MissingParametersError(error_list)

    r = requests.post(url, headers=headers, json=defect_spec)
    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()


# Update defect method.
def update_defect(client, defect_spec, defect_id):
    url = client.base_url + '/defect/' + str(defect_id)


# Request to delete defect.
def delete_defect(client, defect_id):
    url = client.base_url + '/defect/' + str(defect_id)
    headers = {
        "Authorization": 'Bearer ' + client.token
    }
    r = requests.delete(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()


# Method for grabbing a component ID
def get_component(client, component_name, project_id):
    url = client.base_url + '/defect/jtrac/project/metadata?projectids=' + str(project_id)
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r)

    metadata = r.json()
    project_metadata = metadata[str(project_id)]

    # Iterate over the project metadata to find the object that
    # has all the components.
    component_array_index = ""
    for data_object_index, data_object in project_metadata.items():
        if data_object[0]['name'] == 'component':
            component_array_index = data_object_index
            break

    # Iterate over the components to find the right one.
    component_array = project_metadata[component_array_index]
    for component in component_array:
        if component['option'] == component_name:
            return component

    # If we get to this part, something went wrong.
    raise ResourceNotFoundError("component", component_name)


# Get a single defect.
def get_defect(client, defect_id):
    url = client.base_url + '/defect/' + str(defect_id)
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()
