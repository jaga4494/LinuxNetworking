1. List all MAC addresses and IP addresses of the running VMs. 
2. Resolve all IP and MAC conflicts. 
3. Playbook to create VMs and OVS bridge 
 
First a list of running domains is obtained and for each instance its xml file is parsed to get its MAC address. If this MAC is already present in the existing MAC address list, new address is appended to the duplicate list otherwise it is added to the list of addresses. To get the ip addresses associated with the MAC, arp is run and IPS are grepped. Similarly duplicate mac and ip addresses list are found. We can print the required ip and mac lists now. 

To resolve MAC addresses, each MAC is parsed and corresponding IP lists are obtained. Next private key ssh is set and random MAC is generated. Using ip addr show the interface is found and with ip link set new MAC is set for that interface. 
