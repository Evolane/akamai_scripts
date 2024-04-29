import logging.config
import requests
import logger
def remove_config(baseurl, s):
    configs = getsecconfigs(baseurl, s)
    for conf in configs:
        if conf['name'] == "belgium.evolane.be":
            cid = conf["id"]
            versions = getsecconfigversion(baseurl, s, cid)
            vnumber = len(versions)
            deleted = deleteconfig(baseurl, s, cid)


def getsecconfigs(baseurl, s):

    api_url = f'{baseurl}/appsec/v1/configs'

    try:
        result = s.get(api_url)
        result.raise_for_status()
        json_result = result.json()
        configs = json_result['configurations']
        return configs
    except requests.RequestException as e:
        logger.error(f'An error occurred while getting the configs: {e}')
        return []



def getsecconfigversion(baseurl, s, configId):

    api_url = f'{baseurl}/appsec/v1/configs/{configId}/versions'

    try:
        result = s.get(api_url)
        result.raise_for_status()
        json_result = result.json()
        return json_result["versionList"]
    except requests.RequestException as e:
        logger.error(f'An error occurred while getting the config version: {e}')
        return []



def deleteversion(baseurl, s, configId, versionnumber):

    api_url = f'{baseurl}/appsec/v1/configs/{configId}/versions/{versionnumber}'

    try:
        result = s.delete(api_url)
        result.raise_for_status()
        json_result = result.json()
    except requests.RequestException as e:
        logger.error(f'An error occurred while deleting the version: {e}')
        return []



def deleteconfig(baseurl, s, configId):

    api_url = f'{baseurl}/appsec/v1/configs/{configId}'

    try:
        result = s.delete(api_url)
        result.raise_for_status()
        json_result = result.json()
    except requests.RequestException as e:
        logger.error(f'An error occurred while deleting the version: {e}')
        return []