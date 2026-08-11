from netmiko import ConnectHandler

router_config_map = {
    "192.168.1.25": "R1_bgp.txt",
    "192.168.1.26": "R2_bgp.txt"
}
for ip,conf in router_config_map.items():
    device = {
        "device_type": "cisco_ios",
        "ip": ip,
        "username": "cisco",
        "password": "cisco"
    }
 
    connect = ConnectHandler(**device)

    output = connect.send_config_from_file(conf)
    connect.save_config()
    print(output)
    # Verify BGP neighborship
    output=connect.send_command("show ip bgp summary", use_textfsm=True)
    print(output)
    for i in output:
        if i['state_or_prefixes_received']!='Active':
            print("BGP Neighborship Established")
        else:
            print(f"BGP neighborship is in {i['state_or_prefixes_received']}")
    connect.disconnect()