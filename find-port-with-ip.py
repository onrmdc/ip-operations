import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
import re
from getpass import getpass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


currentuser = input("username: ")
currentpass = getpass("password: ")
devam=1

while devam > 0:
    ip_address = input("ip adresini girin: ")
    ip_control = re.findall(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", ip_address)
    if ip_control:
        devicelist = ['10.90.0.191', '10.90.0.192', '10.90.0.161']
        devicelist2 = ['10.90.0.191', '10.90.0.192', '10.90.0.151', '10.90.0.152', '10.90.0.153', '10.90.0.154', '10.90.0.155', '10.90.0.156', '10.90.0.157', '10.90.0.158', '10.90.0.159', '10.90.0.160', '10.90.0.161', '10.90.0.162']

        get_hostname = ['enable', 'show hostname']
        get_ip = ['enable', 'show arp ' + ip_address]
        ping_ip = ['enable', 'ping ' + ip_address]

        outputlist = []

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
            r = requests.post('https://' + switch + '/command-api', data=json.dumps(jsondata), verify=False,
                            auth=HTTPBasicAuth(currentuser, currentpass))
            return json.loads(r.text)

        def main():
            for switch in devicelist:
                ping = eapi(switch, ping_ip)
                hostname = eapi(switch, get_hostname)['result'][1]['hostname']
                ip_to_mac1 = eapi(switch, get_ip)
                if len(ip_to_mac1['result'][1]['ipV4Neighbors']) > 0:
                    ip_to_mac2 = ip_to_mac1['result'][1]['ipV4Neighbors'][0]['hwAddress']
                    ip_to_mac3 = ip_to_mac2.replace('.','')
                    ip_to_mac4 = ':'.join(ip_to_mac3[i:i + 2] for i in range(0, len(ip_to_mac3), 2))
                    print(hostname + ' : Bu IP nin Mac adresi ' + ip_to_mac4)
                else:
                    #print(hostname + ' : IP bu Switchin ARP tablosunda degil')
                    print('-')

            if len(ip_to_mac1['result'][1]['ipV4Neighbors']) > 0:
                for switch in devicelist2:
                    # macden port bulma baslangici
                    hostname = eapi(switch, get_hostname)['result'][1]['hostname']
                    get_interface = ['enable', 'show mac address-table address ' + ip_to_mac4]
                    mac_to_eth1 = eapi(switch, get_interface)
                    if len(mac_to_eth1['result'][1]['unicastTable']['tableEntries']) > 0:
                        mac_to_eth2 = mac_to_eth1['result'][1]['unicastTable']['tableEntries'][0]['interface']
                        print(hostname + ' : Interface ' + mac_to_eth2)
                    else:
                        #print(hostname + ' : MAC bu switchte degil')
                        print('-')
                    # macden port bulma sonu
            else:
                print('IP kullanilmiyor')



        if __name__ == "__main__":
            main()
    else:
        print("IP adresi hatali formatta girildi")


    devamke = input("Devam etmek istiyor musunuz? Y/N ")
    if devamke == "Y" or devamke =="y":
        devam=devam+1
    else:
        devam=0
