#!/usr/bin/env python3
import argparse
import json
import logging.config
import time
from configparser import ConfigParser
from datetime import datetime, timezone, timedelta

import requests
from akamai.edgegrid import EdgeGridAuth
from akamaihostnames import get_akamai_hostnames

def main():
    customer, interval, config, s, baseurl, updown, args, propertyarg = setup()
    api_timeout = 50
    hostnames = get_akamai_hostnames(customer, baseurl, s, api_timeout)



def parse_args():
    parser = argparse.ArgumentParser(description="updown akamai sync.")
    parser.add_argument('--customer', '-c', required=True, help='The customer to execute the tools for')
    parser.add_argument('--dryrun', '-n', default=False, action='store_true',
                        help="dry run = don't sync just get and check all data")
    parser.add_argument('--configfile', '-f', default="config.ini",
                        help="config file path, defaults to config.ini in current dir")
    parser.add_argument('--property', '-p', default=None, help='the chosen Akamai property')
    args = parser.parse_args()
    return args


def parse_config(filename) -> ConfigParser:
    config = ConfigParser()
    config.read(filename)
    return config



def setup():
    """
       Set up the Global variables.
    """
    global args
    args = parse_args()
    customer = args.customer
    interval = args.interval
    propertyarg = args.property
    config = parse_config(args.configfile)
    s = requests.Session()
    baseurl = config[customer]["host"]
    updown = config["main"]["updownApi"]
    s.auth = EdgeGridAuth(
        client_token=config[customer]["client_token"],
        client_secret=config[customer]["client_secret"],
        access_token=config[customer]["access_token"]
    )
    return customer, interval, config, s, baseurl, updown, args, propertyarg



if __name__ == '__main__':
    main()