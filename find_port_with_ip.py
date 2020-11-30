import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
import re
import pprint
import os
from getpass import getpass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#currentuser = input("username: ")
#currentpass = getpass("password: ")
#ip_address = input("ip_address: ")

currentuser = os.environ["NETUSER"]
currentpass = os.environ["NETPASS"]


def eapi(switch, cmds):
    jsondata = {
        "jsonrpc": "2.0",
        "method": "runCmds",
        "params": {
            "format": "json",
            "timestamps": False,
            "autoComplete": False,
            "expandAliases": False,
            "cmds": cmds,
            "version": 1
        },
        "id": "EapiExplorer-1"
    }
    r = requests.post('https://' + switch + '/command-api', data=json.dumps(jsondata),
                      verify=False, auth=HTTPBasicAuth(currentuser, currentpass))
    return json.loads(r.text)

# change for mac search 1
# ARP Table
with open('/project/arp_device_list.txt', 'r') as f:
    content = f.read()
    devicelist = content.splitlines()

# MAC Address Table
with open('/project/mac_device_list.txt', 'r') as f:
    content = f.read()
    devicelist2 = content.splitlines()


def main_func(input_address):
    get_hostname = ['enable', 'show hostname']
    return_dict = {}
    # change for mac search 2
    if validate_ip(input_address):
        print('detect ip address in input box')
        get_ip = ['enable', 'show arp ' + input_address]

        ip_to_mac_api_result = ""
        return_dict['arp'] = []
        ip_to_mac_output = ""
        for switch in devicelist:
            ping_ip = ["enable", "ping {} repeat 1".format(input_address)]
            eapi(switch, ping_ip)
            hostname = eapi(switch, get_hostname)['result'][1]['hostname']
            ip_to_mac_api_result = eapi(switch, get_ip)
            if len(ip_to_mac_api_result['result'][1]['ipV4Neighbors']) > 0:
                ip_to_mac_output = ip_to_mac_api_result['result'][1]['ipV4Neighbors'][0]['hwAddress']
                ip_to_mac_output = ip_to_mac_output.replace('.', '')
                ip_to_mac_output = ':'.join(ip_to_mac_output[i:i + 2] for i in range(0, len(ip_to_mac_output), 2))

                print(hostname + ' : Bu IP nin Mac adresi ' + ip_to_mac_output)
                # MAC addresses extracted from ARP Tables
                return_dict['arp'].append(ip_to_mac_output)
                #print(ip_to_mac_api_result)

            else:
                # print(hostname + ' : IP bu Switchin ARP tablosunda degil')
                print('-')

    # change for mac search 4
    elif validate_mac(input_address):
        print('detect mac address in input box')
        return_dict['arp'] = []
        ip_to_mac_api_result = True
        ip_to_mac_output = input_address
        print(' : Bu IP nin Mac adresi ' + ip_to_mac_output)
        # MAC addresses extracted from ARP Tables
        return_dict['arp'].append(ip_to_mac_output)
    else:
        return 'Invalid IP or MAC Address'

    if ip_to_mac_api_result:
        #if len(ip_to_mac_api_result['result'][1]['ipV4Neighbors']) > 0:
        if ip_to_mac_output:
            return_dict['host_ports'] = []
            for i, switch in enumerate(devicelist2):
                # macden port bulma baslangici
                host_dict = {}
                hostname = eapi(switch, get_hostname)['result'][1]['hostname']
                get_interface = ['enable', 'show mac address-table address ' + ip_to_mac_output]
                mac_to_eth1 = eapi(switch, get_interface)
                if len(mac_to_eth1['result'][1]['unicastTable']['tableEntries']) > 0:
                    host_dict['hostname'] = hostname
                    mac_to_eth2 = mac_to_eth1['result'][1]['unicastTable']['tableEntries'][0]['interface']
                    host_dict['logical'] = mac_to_eth2
                    if 'Port-Channel' in mac_to_eth2:
                        po_number = mac_to_eth2.split('Channel')[-1]
                        if int(po_number) <= 100:
                            continue
                        get_po_bound_ints_cmd = ['enable', 'show port-channel {} all-ports '.format(po_number)]
                        get_po_bound_ints = eapi(switch, get_po_bound_ints_cmd)
                        host_dict['actives'] = " ".join(get_po_bound_ints['result'][1]['portChannels'][mac_to_eth2]['activePorts'].keys())
                        host_dict['inactives'] = " ".join(get_po_bound_ints['result'][1]['portChannels'][mac_to_eth2]['inactivePorts'].keys())
                    print(hostname + ' : Interface ' + mac_to_eth2)
                    return_dict['host_ports'].append(host_dict)

                else:
                    # print(hostname + ' : MAC bu switchte degil')
                    print('-')
                # macden port bulma sonu
        else:
            print('IP kullanilmiyor')

    pprint.pprint(return_dict)
    return return_dict


def validate_ip(ip_address):
    result = re.findall(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", ip_address)
    return result
def validate_mac(mac_address):
    result = re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac_address)
    return result

#main_func(ip_address)
