import logging.config
import requests
import logger

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)
def get_dnssec(baseurl: str, zone , s) -> list:
    """
       Get the DNSSEC status from akamai.

       Returns:
           A list of DNS Records from the client.
    """
    api_url = f'{baseurl}/config-dns/v2/zones/dns-sec-status'

    headers = {
        "PAPI-Use-Prefixes": "false"
    }
    try:
        result = s.get(api_url, headers = headers)
        result.raise_for_status()
        json_result = result.json()
        return json_result
    except requests.RequestException as e:
        logger.error(f'An error occurred while getting the groups: {e}')
        return []



def get_zones(baseurl: str, s) -> list:
    """
       Get the Zones status from akamai.

       Returns:
           A list of zones from the client.
    """
    api_url = f'{baseurl}/config-dns/v2/zones'
    try:
        result = s.get(api_url)
        result.raise_for_status()
        json_result = result.json()
        return json_result['zones']
    except requests.RequestException as e:
        logger.error(f'An error occurred while getting the groups: {e}')
        return []