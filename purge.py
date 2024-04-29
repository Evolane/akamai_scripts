import logging.config
import requests
import logger

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def purge(baseurl: str, s, cpcode, network):
    """
           Purges the cache for a given cp code
        """
    payload = {
        "objects": [
            cpcode
        ]
    }
    #cp = getcpcode(baseurl, s)
    api_url = f'{baseurl}/ccu/v3/delete/cpcode/{network}'

    try:
        result = s.post(api_url, json=payload)
        result.raise_for_status()
        json_result = result.json()
    except requests.RequestException as e:
        logger.error(f'An error occurred while getting the groups: {e}')
        return []


def getcpcode(baseurl, s, cpname):
    """
               Get the cp code id for a given name
            """

    api_url = f'{baseurl}/cprg/v1/cpcodes'

    try:
        result = s.get(api_url)
        result.raise_for_status()
        json_result = result.json()
        for cp in json_result['cpcodes']:
            if cp['cpcodeName'] == cpname:
                return cp['cpcodeId']
        print(json_result)
    except requests.RequestException as e:
        logger.error(f'An error occurred while getting the groups: {e}')
        return []
