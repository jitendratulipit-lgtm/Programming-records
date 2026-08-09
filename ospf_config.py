from netmiko import ConnectHandler
router_config_map = {
    "192.168.1.25": "R1_ospf.txt",
    "192.168.1.26": "R2_ospf.txt"

}

for ip, conf in router_config_map.items():
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
    # Verify OSPF neighborship
    output=connect.send_command("show ip ospf neighbor", use_textfsm=True)
    print(output)
    for i in output:
        if i['state']=='FULL':
            print("OSPF Neighborship Established")
        else:
            print(f"OSPF neighborship is in {i['state']}")
    connect.disconnect()
    
