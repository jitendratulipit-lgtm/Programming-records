import datetime
import os
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, NetMikoAuthenticationException
from paramiko import SSHException

def backup_devices(file_name, backup_dir_path, TNOW):
    """Backup configs for all devices listed in file_name."""
    with open(file_name, "r") as device_file:
        for ip in device_file:
            device = {
                "device_type": "cisco_ios",
                "ip": ip.strip(),
                "username": "cisco",
                "password": "cisco",
            }
            print(f"Connecting to {device['ip']} from {file_name}...")
            try:
                net_connect = ConnectHandler(**device)
                output = net_connect.send_command("show running-config")
                backup_file_path = os.path.join(backup_dir_path, f"{device['ip']}_backup.txt")
                with open(backup_file_path, "w") as backup_file:
                    backup_file.write(output)
                print(f"Backup completed for {device['ip']} → {backup_file_path}")
            except NetMikoTimeoutException:
                print(f"{device['ip']} not reachable")
            except NetMikoAuthenticationException:
                print(f"Authentication failed for {device['ip']}")
            except SSHException:
                print(f"SSH not enabled on {device['ip']}")
            except Exception as e:
                print(f"Unexpected error with {device['ip']}: {e}")

def Backup():
    TNOW = datetime.datetime.now().replace(microsecond=0)
    current_time = TNOW.strftime("%Y-%m-%d_%H-%M-%S")

    backup_dir_path = os.path.join("Device_Backups", current_time)
    os.makedirs(backup_dir_path, exist_ok=True)

    print(f"Starting backup at {TNOW}")

    # Calling helper function twice
    backup_devices("Device_List_routers.txt", backup_dir_path, TNOW)
    backup_devices("Device_List_switches.txt", backup_dir_path, TNOW)

Backup()
