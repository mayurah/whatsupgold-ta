# encoding = utf-8
#

"""Implement your data collection logic here

# The following examples get the arguments of this input.
# Note, for single instance mod input, args will be returned as a dict.
# For multi instance mod input, args will be returned as a single value.
opt_endpoint = helper.get_arg('endpoint')
# In single instance mode, to get arguments of a particular input, use
opt_endpoint = helper.get_arg('endpoint', stanza_name)

# get input type
helper.get_input_type()

# The following examples get input stanzas.
# get all detailed input stanzas
helper.get_input_stanza()
# get specific input stanza with stanza name
helper.get_input_stanza(stanza_name)
# get all stanza names
helper.get_input_stanza_names()


# The following examples get options from setup page configuration.
# get the loglevel from the setup page
loglevel = helper.get_log_level()
# get proxy setting configuration
proxy_settings = helper.get_proxy()
# get account credentials as dictionary
account = helper.get_user_credential_by_username("username")
account = helper.get_user_credential_by_id("account id")
# get global variable configuration
global_whatsup_gold_endpoint_url = helper.get_global_setting("whatsup_gold_endpoint_url")
global_whatsup_gold_username = helper.get_global_setting("whatsup_gold_username")
global_whatsup_gold_password = helper.get_global_setting("whatsup_gold_password")

# The following examples show usage of logging related helper functions.
"""
import os
import sys
import time
import datetime
import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings()


SOURCETYPE_WG_ERR = "progress:whatsupgold:internal:error"
SOURCETYPE_WG_DEBUG = "progress:whatsupgold:internal:debug"
SOURCETYPE_WG_VERSION = "progress:whatsupgold:internal:version"
SOURCETYPE_WG_GROUPS = "progress:whatsupgold:general:groups"
SOURCETYPE_WG_DEVICES = "progress:whatsupgold:general:devices"
TOKEN_ENDPOINT = "/api/v1/token"
TIME_RANGE = "today"
MIN_LENGTH = 1
ACCESS_TOKEN = ""
IS_DEBUG_ENABLED = False
OPT_BASEURL = " "
RANGE_N = "1"

group_id = [ '72', '52', '213', '215']
devices_id = [ '875', '876', '1058', '1059', '1060', '1061', '1062', '1063', '1064', '1066', '1067', '1068', '1069', '1070', '1072', '1073', '1074', '1075', '1076', '1077', '1078', '1079', '1219', '1453', '1595', '1596', '1597', '1598', '1599', '1600', '1601', '1602', '1603', '1604', '1605', '1606', '1607', '1608', '1609', '1610', '1611', '1612', '1613', '1614', '1615', '1616', '1617', '1631', '1632', '1633', '1634', '1635', '1636', '2069', '2070', '2072', '2073', '2074', '2075', '2076', '2077', '2078', '2079', '2080', '2081', '2082', '2083', '2084', '2085', '2086', '2087', '2088', '2089', '2090', '2091', '2092', '2093', '2094', '2095', '2096', '2097', '2098', '2099', '2100', '2101', '2102', '2103', '2104', '2105', '2106', '2107', '2108', '2109', '2110', '2111', '2112', '2113', '2114', '2115', '2116', '2117', '2118', '2119', '2120', '1621', '1627', '1629', '1620', '1630', '1623', '1624', '1618', '1626', '1619', '1628', '1625', '1622', '920' ] 


def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # endpoint = definition.parameters.get('endpoint', None)
    pass

def collect_events(helper, ew):
    
    def log(message, sourcetype=None, exception=False, debug=False):
        
        if type(message) is dict:
            message =  json.dumps(message)
            
        if type(message) is list:
            message =  str(message)

        if sourcetype is None:
            sourcetype=helper.get_sourcetype()
    
        if debug == True:
            sourcetype = SOURCETYPE_WG_DEBUG
            if bool(IS_DEBUG_ENABLED) is False:
                return

        if exception == True:
            sourcetype = SOURCETYPE_WG_ERR

        event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=sourcetype, data=message)
        ew.write_event(event)

    def api_call(endpoint, method="GET"):
        try:
            url = f'{OPT_BASEURL}/{endpoint}'
            payload={}
            headers = {
              'Accept': 'application/json',
              'Authorization': f'Bearer {ACCESS_TOKEN}',
            }
            
            r = requests.request("GET", url, headers=headers, data=payload)
            
            if r.status_code not in (200,302):
                log(r.status_code, SOURCETYPE_WG_VERSION)
                log(r.text, SOURCETYPE_WG_VERSION)
                return " Error "
        
            
            return json.loads(r.text)
        except Exception as e:
            log(str(e), exception=True)
            return " Exception "

    # 10.202.12.8
    wug_api_endpoint = helper.get_global_setting("whatsup_gold_api_endpoint")
    wug_web_endpoint = helper.get_global_setting("whatsup_gold_web_endpoint")
    wug_username = helper.get_global_setting("whatsup_gold_username")
    wug_password = helper.get_global_setting("whatsup_gold_password")
    # OPT_ENDPOINT = helper.get_arg('endpoint')
    OPT_BASEURL = wug_api_endpoint
    IS_DEBUG_ENABLED = str(helper.get_arg('debug'))
    TIME_RANGE = helper.get_arg('time_range')
    RANGE_N = helper.get_arg('range_n')
    device_reports = helper.get_arg('device_reports')


    log("TA Init - 2.0.1", debug=True)


    def generate_token():
        try:
            url = f"{wug_api_endpoint}/{TOKEN_ENDPOINT}"
            
            payload = f"grant_type=password&username={wug_username}&password={wug_password}"
            # log(payload, debug=True)
            headers = {
              'Accept': '*/*',
              'Accept-Language': 'en-US,en;q=0.9',
              'Connection': 'keep-alive',
              'X-Requested-With': 'XMLHttpRequest'
            }
            
            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code not in (200,302):
                log(response.text, SOURCETYPE_WG_VERSION)
 
            return json.loads(response.text)['access_token']
        except Exception as e:
                log(str(e), exception=True)
    
        return response.text
        
    # Get WUG version
    def get_version():

        try:
            url = f"{wug_api_endpoint}/api/v1/product/version"
            payload={}
            headers = {
              'Accept': 'application/json',
              'Authorization': f'Bearer {ACCESS_TOKEN}',
            }
            
            # log(str(headers))
            
            response = requests.request("GET", url, headers=headers, data=payload)
            
            if response.status_code not in (200,302):
                log(response.text, SOURCETYPE_WG_VERSION)
        
            
            return json.loads(response.text)["data"]
        except Exception as e:
            log(str(e), exception=True)
            return " Exception "
            
        return response.text
        
        
        
    # Get Groups
    def get_groups():
        ## endpoint = "/api/v1/device-groups/-?limit=10000"
        ## groups = api_call(endpoint)
        
        ## for group in groups["data"]["groups"]:
        ##    log(group, SOURCETYPE_WG_GROUPS)
        ##    # get_devices(group["id"])

        for group in group_id:
            # log(group, SOURCETYPE_WG_GROUPS)
            get_devices(group)
        
        
    # Get Devices for given group
    def get_devices(group_id):
        endpoint = f"/api/v1/device-groups/{group_id}/devices/-?view=card&limit=10000"
        devices = api_call(endpoint)
        devices_data = devices["data"]["devices"]
        
        if len(devices_data) >= MIN_LENGTH:
            for device in devices["data"]["devices"]:
                log(device, SOURCETYPE_WG_DEVICES)
                if int(device["id"]) in devices_id:
                    get_additional_data(device["id"]) # device["id"]
                else:
                    log(f' {device["id"]} not in devices_id', SOURCETYPE_WG_DEVICES)
            
    
    # Get Devices for given group
    def get_additional_data(device_id):
        endpoints = {
          "cpu-utilization": f"/api/v1/devices/{device_id}/reports/cpu-utilization?range={TIME_RANGE}&rangeN={RANGE_N}",
          "disk-free-space": f"/api/v1/devices/{device_id}/reports/disk-free-space?range={TIME_RANGE}&rangeN={RANGE_N}",
          "disk-utilization": f"/api/v1/devices/{device_id}/reports/disk-utilization?range={TIME_RANGE}&rangeN={RANGE_N}",
          "interface-discards": f"/api/v1/devices/{device_id}/reports/interface-discards?range={TIME_RANGE}&rangeN={RANGE_N}",
          "interface-errors": f"/api/v1/devices/{device_id}/reports/interface-errors?range={TIME_RANGE}&rangeN={RANGE_N}",
          "interface-traffic": f"/api/v1/devices/{device_id}/reports/interface-traffic?range={TIME_RANGE}&rangeN={RANGE_N}",
          "interface-utilization": f"/api/v1/devices/{device_id}/reports/interface-utilization?range={TIME_RANGE}&rangeN={RANGE_N}",
          "memory-utilization": f"/api/v1/devices/{device_id}/reports/memory-utilization?range={TIME_RANGE}&rangeN={RANGE_N}",
          "ping-availability": f"/api/v1/devices/{device_id}/reports/ping-availability?range={TIME_RANGE}&rangeN={RANGE_N}",
          "response-time": f"/api/v1/devices/{device_id}/reports/ping-response-time?range={TIME_RANGE}&rangeN={RANGE_N}",
          "state-change": f"/api/v1/devices/{device_id}/reports/state-change?range={TIME_RANGE}&rangeN={RANGE_N}"
            }


        for sourcetype in endpoints:
            if sourcetype in device_reports:
                endpoint = endpoints[sourcetype]
                # log(endpoints, debug=True)
                metadata = api_call(endpoint)["data"]
                if len(metadata) >= MIN_LENGTH:
                    for event in metadata:
                        log(event, sourcetype=f"progress:whatsupgold:{sourcetype}")

    # Generate Token
    ACCESS_TOKEN = generate_token()
    #log(ACCESS_TOKEN + "asd")
    # Get Version
    log(get_version(), debug=True)
    get_groups()
    
    
    # auth = HTTPBasicAuth(global_whatsup_gold_username, global_whatsup_gold_password)
    # for endpoint in opt_endpoint.split(","):
    #     url = f'{global_whatsup_gold_endpoint_url}/{opt_endpoint.strip()}'
    #     url = url.replace('///','/')
    #     api_call("GET", url, auth)
    
    
    """
    # write to the log for this modular input using configured global log level or INFO as default
    helper.log("log message")
    # write to the log using specified log level
    helper.log_debug("log message")
    helper.log_info("log message")
    helper.log_warning("log message")
    helper.log_error("log message")
    helper.log_critical("log message")
    # set the log level for this modular input
    # (log_level can be "debug", "info", "warning", "error" or "critical", case insensitive)
    helper.set_log_level(log_level)

    # The following examples send rest requests to some endpoint.
    response = helper.send_http_request(url, method, parameters=None, payload=None,
                                        headers=None, cookies=None, verify=True, cert=None,
                                        timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()

    # The following examples show usage of check pointing related helper functions.
    # save checkpoint
    helper.save_check_point(key, state)
    # delete checkpoint
    helper.delete_check_point(key)
    # get checkpoint
    state = helper.get_check_point(key)

    # To create a splunk event
    helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    """

    '''
    # The following example writes a random number as an event. (Multi Instance Mode)
    # Use this code template by default.
    import random
    data = str(random.randint(0,100))
    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)
    ew.write_event(event)
    '''

    '''
    # The following example writes a random number as an event for each input config. (Single Instance Mode)
    # For advanced users, if you want to create single instance mod input, please use this code template.
    # Also, you need to uncomment use_single_instance_mode() above.
    import random
    input_type = helper.get_input_type()
    for stanza_name in helper.get_input_stanza_names():
        data = str(random.randint(0,100))
        event = helper.new_event(source=input_type, index=helper.get_output_index(stanza_name), sourcetype=helper.get_sourcetype(stanza_name), data=data)
        ew.write_event(event)
    '''
