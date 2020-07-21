import json, os, pathlib
from collections.abc import Iterable

mac = "229e"
key = "123" # switch id
with open(os.path.join(pathlib.Path(__file__).parent.absolute(), 'mac_address_resp_example.json')) as json_file:
    show_mac_address_table_resp = json.load(json_file)
for nic_name,nic_value in show_mac_address_table_resp['msg'].items():
    if isinstance(nic_value, Iterable):
        if 'mac_entries' in nic_value:
            for curr_mac in nic_value['mac_entries']:
                if curr_mac['mac_address'].find(mac) >= 0:
                    print(dict(switch_id=int(key), interface=nic_name))