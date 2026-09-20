import json
from napalm import get_network_driver

driver = get_network_driver("ios")

# Read IPs from device_list.txt
with open("Device_List_routers.txt") as f:
    ips = f.read().splitlines()

# Loop through each IP and connect
for ip in ips:
    try:
        device = driver(ip, "cisco", "cisco")   # username/password can be parameterized
        device.open()

        routes = device.get_route_to(destination= "", protocol= "bgp")  # structured dict
        print(f"\nRouting table for {ip}:\n")
        print(json.dumps(routes, indent=4))  # pretty JSON output

        device.close()
    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")
