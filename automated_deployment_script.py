from netmiko import ConnectHandler

import re
import sys
import paramiko
fd = open(r'C:\Users\Chris\\PythonOutput.txt','w')
sys.stdout = fd 
platform = 'cisco_ios'
username = 'admin'
password = 'admin'

#this function will assist in getting a unique ID for the device.  
def SerialNumber():
    showIP = device.send_command("show version | i ID")
    r1 = re.search(r"[^D ]*$", showIP)
    xy = r1.group()
    device.send_config_set('file prompt quiet')
    device.send_command('copy tftp://172.16.1.21/' +xy+ '/switch-config flash:/switch-config')
    return(xy)

#this function will look at firmware and download/set new firmware when needed
def Version():
    showIP = device.send_command("show version | i image")
    r1 = re.search(r'(?<=\/).*?(?=")', showIP)
    xy = r1.group()
    if xy == "vios_l2-adventerprisek9-m":
        device.send_config_set('file prompt quiet')
        device.send_command('copy tftp://172.16.1.21/IOS/vios_l2-adventerprisek9-m flash:/vios_l2-adventerprisek9-m')
        device.send_config_set('boot system flash:/vios_l2-adventerprisek9-m')
        print("Done!")
    return(xy)

#this will set the new config after reload.
def CopyConfig():
    device.send_command('copy flash0:/switch-config startup-config')

#reloads the switch
def Reload():
    device.send_command('reload', expect_string='confirm')
    device.send_command('\n')

##Make this the directory of the IPlist.txt
ip_add_file = open(r'C:\Users\Chris\\IPAddressList.txt','r')

for host in ip_add_file:
        device = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
        SerialNumber()
        Version()
        print(SerialNumber())
        print(Version())
        #CopyConfig()
        #Reload()

fd.close()


