from netmiko import ConnectHandler
import os
from ttp import ttp
import json

Base_BGP_logs = "BGP_Logs"
os.makedirs(Base_BGP_logs, exist_ok=True)

with open("Device_List_routers.txt") as DEVICE_LIST:
    for IP in DEVICE_LIST:
        RTR={
            "ip":IP.strip(),
            "username":"cisco",
            "password":"cisco",
            "device_type":"cisco_ios"
        }
        try:
            connect=ConnectHandler(**RTR)
            output=connect.send_command("show ip bgp summary", use_textfsm=True)
            for i in output:
                if i['state_or_prefixes_received']!='Idle':
                    output=connect.send_command("show ip route bgp")
                    filename = os.path.join(Base_BGP_logs, f"{IP.strip()}_bgp_logs.txt")
                    with open(filename, "w") as logs:
                        logs.write(output)
                    print(f"BGP Logs from {IP.strip()} saved to {filename}")
                else:
                    print(f"BGP neighborship is in {i['state_or_prefixes_received']}")
            

            connect.disconnect()

        except Exception as e:
            print(f"Error connecting to {IP.strip()}: {e}")
            
parsed_outputs = []

template = """
{{ protocol | re("B") }} {{ prefix | IP }} [{{ metric }}] via {{ nexthop | IP }}, {{ uptime }}
"""

# Parse Router 1 logs
with open("BGP_Logs\\192.168.1.25_bgp_logs.txt","r") as file:
    logs = file.read()
    parser = ttp(data=logs, template=template)
    parser.parse()
    results = parser.result(format="json")
    structured_output = json.loads(results[0])
    parsed_outputs.append(structured_output[0])   # Router 1 routes

# Parse Router 2 logs
with open("BGP_Logs\\192.168.1.26_bgp_logs.txt","r") as file:
    logs = file.read()
    parser = ttp(data=logs, template=template)
    parser.parse()
    results = parser.result(format="json")
    structured_output = json.loads(results[0])
    parsed_outputs.append(structured_output[0])   # Router 2 routes

# Build dictionaries keyed by prefix
r1_routes = {}
for route in parsed_outputs[0]:
    r1_routes[route['prefix']] = route

r2_routes = {}
for route in parsed_outputs[1]:
    r2_routes[route['prefix']] = route

# Consistency check
print("\n🔎 Consistency Check Results:")
for prefix in r1_routes:
    if prefix not in r2_routes:
        print(f"- Prefix {prefix} missing in Router 2")
    else:
        if r1_routes[prefix]['metric'] == r2_routes[prefix]['metric']:
            print(f"- {prefix}: ✅ Metric consistent ({r1_routes[prefix]['metric']})")
        else:
            print(f"- {prefix}: ❌ Metric mismatch (R1={r1_routes[prefix]['metric']}, R2={r2_routes[prefix]['metric']})")
