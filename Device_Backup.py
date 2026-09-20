import datetime
import os
import time
from netmiko import ConnectHandler

def Backup():
    TNOW = datetime.datetime.now().replace(microsecond=0)
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")

    #create backup directory based on date
    backup_dir_path = os.path.join("Device_Backups", current_time)
    # Make the directory
    os.makedirs(backup_dir_path, exist_ok=True)
    #print(f"Backup directory created: {backup_dir_path}")

    print(f"Taking backup of Routers at {TNOW}")

    with open("Device_List_routers.txt", "r") as device_file:
        for ip in device_file:
            device = {
                "device_type": "cisco_ios",
                "ip": ip.strip(),
                "username": "cisco",
                "password": "cisco",
            }
            print(f"Connecting to Router: {device['ip']}")
            try:
                net_connect = ConnectHandler(**device)
                output = net_connect.send_command("show running-config")
                backup_file_path = os.path.join(backup_dir_path, f"{device['ip']}_router_backup.txt")
                with open(backup_file_path, "w") as backup_file:
                    backup_file.write(output)
                print(f"Backup completed for Router: {device['ip']}. Saved to {backup_file_path}")
            except Exception as e:
                print(f"Failed to connect to Router {device['ip']}: {e}")

    print(f"Taking backup of Switches at {TNOW}")

    with open("Device_List_switches.txt", "r") as device_file:
        for ip in device_file:
            device = {
                "device_type": "cisco_ios",
                "ip": ip.strip(),
                "username": "cisco",
                "password": "cisco",
            }
            print(f"Connecting to Switch: {device['ip']}")
            try:
                net_connect = ConnectHandler(**device)
                output = net_connect.send_command("show running-config")
                backup_file_path = os.path.join(backup_dir_path, f"{device['ip']}_switch_backup.txt")
                with open(backup_file_path, "w") as backup_file:
                    backup_file.write(output)
                print(f"Backup completed for Switch: {device['ip']}. Saved to {backup_file_path}")
            except Exception as e:
                print(f"Failed to connect to Switch {device['ip']}: {e}")
Backup()
