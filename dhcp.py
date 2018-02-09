import subprocess
import logging
import random
import sys
import time


logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
logging.getLogger("scapy.interactive").setLevel(logging.ERROR)
logging.getLogger("scapy.loading").setLevel(logging.ERROR)


try:
    from scapy.all import *

except ImportError:
    print "Scapy package for Python is not installed on your system."
    print "Get it from https://pypi.python.org/pypi/scapy and try again."
    sys.exit()
    

print "\n! Make sure to run this program as ROOT !\n"

#Setting network interface in promiscuous mode

    
net_iface = raw_input("Enter the interface to the target network: ")
exitcode = subprocess.call(["ifconfig", net_iface, "promisc"], stdout=None, stderr=None, shell=False)
if (exitcode != 0):
    print "\nNo such device \n"
    sys.exit()

print "\nInterface %s was set to PROMISC mode." % net_iface
conf.checkIPaddr = False

#global leased_ips
global server_id
global mac_address
global leased_ips
leased_ips =[]
server_id = []
mac_address = []

def dhcp_request():
    
    x_id = random.randrange(1, 1000000)
    hw = "00:00:5e" + str(RandMAC())[8:]
    hw_str = mac2str(hw)
    #sending dhcp discovey packet
    dhcp_dis_pkt = Ether(dst="ff:ff:ff:ff:ff:ff",src=hw )/IP(src="0.0.0.0", dst="255.255.255.255")/UDP(sport='bootpc',dport='bootps')/BOOTP(op = 'BOOTREQUEST', xid = x_id, chaddr = hw_str )/ DHCP(options=[("message-type","discover"),("end")])
    print "\nsending dhcp discovery packet\n"
    answd, unanswd = srp(dhcp_dis_pkt, iface=net_iface, timeout = 2.5, multi = True)
    #print answd
    if (len(answd) > 1):
        print "There are more than one dhcp servers in LAN\n"
        permission = raw_input ("Do you want to quit and check DHCP servers(y/n)\n")
        while (permission != "y") and (permission != "n"):
            permission = raw_input("\nplease type y or n: \n")
        if (permission == "y"):
            sys.exit()
        elif(permission == "n"):
           print " "
            
    try:    
        offered_ip = answd[0][1][BOOTP].yiaddr
        server_ip = answd[0][1][IP].src
        #print "%s %s %s" %(offered_ip,server_ip,hw)
        #sending dhcp request packet
        
        dhcp_req_pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src=hw)/IP(src="0.0.0.0",dst="255.255.255.255") / UDP(sport=68,dport=67)/BOOTP(op="BOOTREQUEST", xid=x_id, chaddr=hw_str)/DHCP(options=[("message-type","request"),("server_id",server_ip),("requested_addr", offered_ip),("end")])
        print "\nSending request packet:\n"
        answr, unanswr = srp(dhcp_req_pkt, iface=net_iface, timeout = 2.5, verbose=0)
        binded_offered_ip_ack = answr[0][1][BOOTP].yiaddr
        server_ip = answr[0][1][IP].src
        #print answr
        #print "\n"
        #print binded_offered_ip_ack
    except IndexError:
        print "\nLink is down or DHCP server is not set.No DHCP offer recieved\n"
        #incase no ip add
        list =["169","254"]
        a = random.randrange(1,254)
        list.append(str(a))
        b = random.randrange(1,254)
        list.append(str(b))
        binded_offered_ip_ack = ":".join(list)
        server_ip = "APIPA IP"
    return binded_offered_ip_ack, server_ip, hw

def generate_dhcp_release(ip, hw, server):

    #Defining DHCP Transaction ID
    x_id = random.randrange(1, 1000000)
    hw_str = mac2str(hw)
    
    #Creating the RELEASE packet
    print "Sending dhcp release pck \n "
    dhcp_release_pkt = IP(src=ip,dst=server) / UDP(sport=68,dport=67)/BOOTP(chaddr=hw_str, ciaddr=ip, xid=x_id)/DHCP(options=[("message-type","release"),("server_id", server),("end")])
    
    #Sending the RELEASE packet
    send(dhcp_release_pkt, verbose=0)
    
try:
    #Enter option for the first screen
    while True:
        print "\nUse this tool to:\ns - Simulate DHCP Clients\nr - Simulate DHCP Release\ne - Exit program\n"
        
        user_option_sim = raw_input("Enter your choice: ")
        
        if user_option_sim == "s":
            print "\nObtained leases will be exported to 'DHCP_Leases.txt'!"
            
            pkt_no = raw_input("\nNumber of DHCP clients to simulate: ")
            
            print "\nWaiting for clients to obtain IP addresses...\n"
            

            #Calling the function for the required number of times (pkt_no)
            for iterate in range(0, int(pkt_no)):
                 
                a = dhcp_request()
                leased_ips.append(a[0])
                server_id.append(a[1])
                mac_address.append(a[2]) 
            
            #print leased_ips
            #print server_id
            #print mac_address
            
            
            for index, each_ip in enumerate(leased_ips):  
                print  "leased ip is :"+each_ip +", "+server_id[index]+", "+mac_address[index] +"\n"
                
    
            
            continue 
        elif user_option_sim == "r":
            user_option_address = raw_input("Enter IP address to release: ")
                    
            try:
                #Check if required IP is in the list and run the release function for it
                if user_option_address in leased_ips:
                    index = leased_ips.index(user_option_address)
                    generate_dhcp_release(user_option_address, mac_address[index], server_id[index])
                    print "\nSending RELEASE packet...\n"
                    leased_ips.pop(index)
                    server_id.pop(index)
                    mac_address.pop(index)
                    
                    for index, each_ip in enumerate(leased_ips):  
                         print  "leased ip is :"+each_ip +", "+server_id[index]+", "+mac_address[index] +"\n"
                
    
                    
                else:
                    print "IP Address not in list.\n"
                    continue
                    
            except (NameError, IndexError):
                print "\nSimulating DHCP RELEASES cannot be done separately, without prior DHCP Client simulation."
                print "Restart the program and simulate DHCP Clients and RELEASES in the same program session.\n"
                sys.exit()
                
        else:
            print "Exiting... See ya...\n\n"
            sys.exit()

except KeyboardInterrupt:
    print "\n\nProgram aborted by user. Exiting...\n"
    sys.exit()         
    

    