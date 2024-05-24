import logging.config
import requests
import logger

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)



def list_api_client(baseurl, s):
    """
       Get the api clients of a customer from akamai.

       Returns:
           A list of all api clients from the client.
    """
    api_url = f'{baseurl}/identity-management/v3/api-clients'

    headers = {
        "accept": "application/vnd.akamai.cps.enrollments.v12+json"
    }
    try:
        result = s.get(api_url, headers = headers)
        result.raise_for_status()
        json_result = result.json()
        return json_result
    except requests.RequestException as e:
        logger.error(f'An error occurred while getting the api clients: {e}')
        return []