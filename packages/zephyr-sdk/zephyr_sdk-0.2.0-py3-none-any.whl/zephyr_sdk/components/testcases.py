import requests
from zephyr_sdk.exceptions.ZExceptions import ZAPIError
from zephyr_sdk.exceptions.ZExceptions import MissingParametersError


# Create a Testcase
def create_testcase(client, testcase_spec):
    url = client.base_url + '/testcase'
    headers = {
        "Authorization": "Bearer " + client.token,
        "Content-Type": "application/json"
    }

    # Validate request body
    error_list = []
    if 'name' not in testcase_spec['testcase']:
        error_list.append("testcase.name")
    if 'tcrCatalogTreeId' not in testcase_spec:
        error_list.append("tcrCatalogTreeId")

    if len(error_list) > 0:
        raise MissingParametersError(error_list)

    r = requests.post(url, headers=headers, json=testcase_spec)
    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()


# Delete Testcase Function
def delete_testcase(client, testcase_id):
    url = client.base_url + '/testcase/' + str(testcase_id)
    headers = {
        "Authorization": "Bearer " + client.token
    }

    r = requests.delete(url, headers=headers)

    if r.status_code != 200:
        raise ZAPIError(r)
    return r.json()


# Get information on testcase function
def get_testcase_by_id(client, testcase_id):
    url = client.base_url + '/testcase/' + str(testcase_id)
    headers = {
        "Authorization": "Bearer " + client.token
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        raise ZAPIError(r)
    return r.json()


def map_testcase_to_requirements(client, map_spec):
    # First validate the map_spec to make sure it has the right values.
    required_parameters = [
        'testcaseId',
        'releaseId',
        'requirementIds',
        'requirementTreeId'
    ]
    error_list = []
    for parameter in required_parameters:
        if parameter not in map_spec:
            error_list.append(parameter)

    if len(error_list) > 0:
        raise MissingParametersError(error_list)

    # Now make the actual API call.
    url = client.base_url + "/testcase/allocate/requirement/" + str(map_spec['testcaseId']) + "?releaseid=" + str(map_spec['releaseId'])
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + client.token
    }

    # Generate the actual request body based on the map_spec object
    requirement_mappings = []
    for req_id in map_spec['requirementIds']:
        requirement_mappings.append([
            map_spec['requirementTreeId'],
            req_id
        ])

    req_body = {
        "modRequirementTree": [
            [
                map_spec['requirementTreeId'],
                0
            ]
        ],
        "testcaseid": map_spec['testcaseId'],
        "releaseId": map_spec['releaseId'],
        "modRequirement": requirement_mappings
    }

    r = requests.post(url, headers=headers, json=req_body)
    if r.status_code != 200:
        raise ZAPIError(r)
    return r.json()


# Update a Testcase
def update_testcase(client, testcase_id, testcase_spec):
    url = client.base_url + '/testcase/' + str(testcase_id)
    headers = {
        "Authorization": "Bearer " + client.token,
        "Content-Type": "application/json"
    }

    # Get info on the testcase
    testcase_info = client.get_testcase_by_id(testcase_id)

    for parameter in testcase_info:
        if parameter not in testcase_spec:
            testcase_spec[parameter] = testcase_info[parameter]

    # Also go through the specific testcase parameters as well.
    for parameter in testcase_info['testcase']:
        if parameter not in testcase_spec['testcase']:
            testcase_spec['testcase'][parameter] = testcase_info['testcase'][parameter]

    r = requests.put(url, headers=headers, json=testcase_spec)
    if r.status_code != 200:
        raise ZAPIError(r)

    return r.json()
