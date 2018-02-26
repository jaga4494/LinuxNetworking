# CreatingVM.sh  

Script first checks whether libvirt, qemu, kvm, bridge, virt and virt-viewer are installed. If not installed install them.
User can enter the VM name, RAM, disk storage, number of vcpu, iso image location, number of interfaces, name of the network. Install VM using above information.
It takes some time to install the VM.  

To delete a VM, uncomment the last 5 lines of the code and run the script. 

# Using Python - Libvirt API:  
1. Host Information.  
2. Guest Domain Information.  
3. Performance monitoring python application to monitor VCPU and VMEM of all VMs and performs following operations:  
(a) print all VMs in ascending order, based on CPU /memory usage.  
(b) print and also log in a file an alert message (Vm name, time stamp, CPU usage) if CPU usage crossed a threshold T (take from user input).  

CPU or MEM is given as the argument to the program and it returns the list of VMs sorted by the given argument.  


prob6.py  
Host information and Domain information are displayed  
Give the domain name as the first argument otherwise libvirt error is thrown   
Example valid input:  
sudo python prob6_3.py <available domain name>  

prob6_3.py  
Execute by using sudo python prob6_3.py Argument1 Argument2  

Argument1 - CPU or MEM.  
Argument2 – Threshold value (valid number)  

Note:  
‘cpu’  or ‘mem’ or any other value does not work for argument1  

Example valid input:  
sudo python prob6_3.py CPU 1000  
sudo python prob6_3.py MEM 2000  

Example Invalid input:  
sudo python prob6_3.py 778 2000  
sudo python prob6_3.py ans 2000  
sudo python prob6_3.py  
sudo python prob6_3.py MEM ddas  


If CPU usage is crosses the input threshold value, cpulogs.log files logs the message in appropriate format and the alert message is also printed.  

Memdict and cpudict dictionaries are used to store the respective usages.  

Based on input (CPU or MEM) , output will be sorted in that order. Even if first argument is wrong, based on threshold value log values are added.  

