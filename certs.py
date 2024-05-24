import logging.config
import requests
import logger

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)



def update_tech_contact(customer, s, baseurl):
    enrollments = listenrollments(baseurl, s)
    for rol in enrollments:
        if rol["csr"]["cn"] == "cert.be":
            #single_rol = getenrolment(baseurl, s, rol["id"])
            temp = updateunrolment(baseurl, s, rol["id"], rol)


def listenrollments(baseurl: str, s):
    """
       Get the enrollments of a customer from akamai.

       Returns:
           A list of all enrollments from the client.
    """
    api_url = f'{baseurl}/cps/v2/enrollments'

    headers = {
        "accept": "application/vnd.akamai.cps.enrollments.v11+json"
    }
    try:
        result = s.get(api_url, headers = headers)
        result.raise_for_status()
        json_result = result.json()
        return json_result["enrollments"]
    except requests.RequestException as e:
        logger.error(f'An error occurred while getting the enrollments: {e}')
        return []



def getenrolment(baseurl: str, s, id):
    """
       Get the enrollments of a customer from akamai.

       Returns:
           A list of all enrollments from the client.
    """
    param = 'thw6chguao2ww4bp'
    api_url = f'{baseurl}/cps/v2/enrollments/{id}'

    headers = {
        "accept": "application/json"
    }
    try:
        result = s.get(api_url, headers=headers)
        result.raise_for_status()
        json_result = result.json()
        return json_result
    except requests.RequestException as e:
        logger.error(f'An error occurred while getting the enrollment: {e}')
        return []



def updateunrolment(baseurl: str, s, id, data):
    """
       update the enrollment of a certificate of a customer from akamai.

       Returns:
           .
    """
    param = 'thw6chguao2ww4bp'
    api_url = f'{baseurl}/cps/v2/enrollments/{id}'

    headers = {
        "accept": "application/json"
    }
    payload = data
    try:
        result = s.put(api_url, headers = headers, data=payload)
        result.raise_for_status()
        json_result = result.json()
        return json_result
    except requests.RequestException as e:
        logger.error(f'An error occurred while getting the enrollment: {e}')
        return []