# DHCP-simulator
#Example
```
root@debian:~# python dhcp.py

! Make sure to run this program as ROOT !

Enter the interface to the target network: eth1 

Interface eth1 was set to PROMISC mode.

Use this tool to:
s - Simulate DHCP Clients
r - Simulate DHCP Release
e - Exit program

Enter your choice: s

Obtained leases will be exported to 'DHCP_Leases.txt'!

Number of DHCP clients to simulate: 3

Waiting for clients to obtain IP addresses...


sending dhcp discovery packet

Begin emission:
Finished to send 1 packets.
..**
Received 4 packets, got 2 answers, remaining 0 packets
There are more than one dhcp servers in LAN

Do you want to quit and check DHCP servers(y/n)
y
root@debian:~# python dhcp.py

! Make sure to run this program as ROOT !

Enter the interface to the target network: eth1

Interface eth1 was set to PROMISC mode.

Use this tool to:
s - Simulate DHCP Clients
r - Simulate DHCP Release
e - Exit program

Enter your choice: s

Obtained leases will be exported to 'DHCP_Leases.txt'!

Number of DHCP clients to simulate: 3

Waiting for clients to obtain IP addresses...


sending dhcp discovery packet

Begin emission:
Finished to send 1 packets.
.*
Received 2 packets, got 1 answers, remaining 0 packets

Sending request packet:


sending dhcp discovery packet

Begin emission:
Finished to send 1 packets.
.*.
Received 3 packets, got 1 answers, remaining 0 packets

Sending request packet:


sending dhcp discovery packet

Begin emission:
Finished to send 1 packets.
.*
Received 2 packets, got 1 answers, remaining 0 packets

Sending request packet:

leased ip is :10.1.1.18, 10.1.1.1, 00:00:5e:bf:b7:0c

leased ip is :10.1.1.19, 10.1.1.1, 00:00:5e:e9:79:36

leased ip is :10.1.1.20, 10.1.1.1, 00:00:5e:b0:57:27


Use this tool to:
s - Simulate DHCP Clients
r - Simulate DHCP Release
e - Exit program

Enter your choice: r
Enter IP address to release: 10.1.1.20
Sending dhcp release pck 
 

Sending RELEASE packet...

leased ip is :10.1.1.18, 10.1.1.1, 00:00:5e:bf:b7:0c

leased ip is :10.1.1.19, 10.1.1.1, 00:00:5e:e9:79:36


Use this tool to:
s - Simulate DHCP Clients
r - Simulate DHCP Release
e - Exit program

Enter your choice: e
Exiting... See ya...

```

