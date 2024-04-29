import logging.config
import requests
import logger

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


Excludedproperties = {
    "bac.netstorage.websites",
    "bac.updown"
}

def get_akamai_hostnames(customer, baseurl: str, s, api_timeout):
    hostnamelist = []
    groups = get_groups(baseurl, s)
    if len(groups) == 0:
        print(f'Er werden geen groepen gevonden voor {customer}, waarschijnlijk zijn de papi tokens vervallen')
        return
    for group in groups:
        properties = get_properties(group["contractIds"][0], group["groupId"],baseurl, s, api_timeout)
        for property in properties:
            if "propertyId" in property:
                if property["productionVersion"] is not None:
                    # logger.info(property["propertyName"])
                    if property["propertyName"] not in Excludedproperties:
                        print(f'de nieuwe hostnames uit property {property["propertyName"]} zullen worden toegevoegd aan Updown')
                        hostnames = get_hostnames(property["propertyId"], property["productionVersion"], baseurl, s, api_timeout)
                        # logger.info(hostnames)
                        for host in hostnames:
                            #print(host["cnameFrom"])
                            hostnamelist.append(host)

    return hostnamelist


def get_groups(baseurl: str, s) -> list:
    """
       Get the groups from akamai.

       Returns:
           A list of groups.
    """
    api_url = f'{baseurl}/papi/v1/groups'
    try:
        result = s.get(api_url)
        result.raise_for_status()
        json_result = result.json()
        return json_result["groups"]["items"]
    except requests.RequestException as e:
        logger.error(f'An error occurred while getting the groups: {e}')
        return []


def get_properties(contractId: str, groupId: str, baseurl: str, s, api_timeout) -> list:
    """
       Get the properties for the given contract ID, and group ID.

       Args:
           contractId: The contract ID.
           groupId: The group ID.

       Returns:
           A list of properties.
    """
    api_url = f'{baseurl}/papi/v1/properties?contractId={contractId}&groupId={groupId}'
    headers = {
        "PAPI-Use-Prefixes": "false"
    }
    try:
        result = s.get(api_url, headers=headers, timeout=api_timeout)
        result.raise_for_status()
        json_result = result.json()
        return json_result["properties"]["items"]
    except (requests.RequestException, ValueError) as e:
        logging.error("An error occurred while getting the properties: %s", e)
        return []


def get_hostnames(propertyId: str, productionVersion: str, baseurl: str, s, api_timeout) -> list:
    """
    Get the hostnames for the given property ID, and production version.

    Args:
        propertyId: The property ID.
        productionVersion: The production version.

    Returns:
        A list of hostnames.
    """

    api_url = f'{baseurl}/papi/v1/properties/{propertyId}/versions/{productionVersion}/hostnames'
    headers = {
        "PAPI-Use-Prefixes": "False"
    }

    try:
        result = s.get(api_url, headers=headers, timeout=api_timeout)
        result.raise_for_status()
        json_result = result.json()
        return json_result["hostnames"]["items"]
    except (requests.RequestException, ValueError) as e:
        logging.error("An error occurred while getting the hostnames: %s", e)
        return []



def get_hostnames_for_property(customer, baseurl: str, s, api_timeout, propertyarg):
    hostnamelist = []
    groups = get_groups(baseurl, s)
    if len(groups) == 0:
        print(f'Er werden geen groepen gevonden voor {customer}, waarschijnlijk zijn de papi tokens vervallen')
        return
    for group in groups:
        properties = get_properties(group["contractIds"][0], group["groupId"],baseurl, s, api_timeout)
        for property in properties:
            if "propertyId" in property:
                if property["productionVersion"] is not None:
                    # logger.info(property["propertyName"])
                    if property["propertyName"] == propertyarg:
                        hostnames = get_hostnames(property["propertyId"], property["productionVersion"], baseurl, s, api_timeout)
                        # logger.info(hostnames)
                        for host in hostnames:
                            #print(host["cnameFrom"])
                            hostnamelist.append(host)

    return hostnamelist
