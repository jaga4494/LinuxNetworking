#!/bin/bash

#To check if libvirt is installed
if [ $(dpkg-query -W -f='${Status}' libvirt-bin 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  apt-get install libvirt-bin;
  echo "Install successful - libvirt"
  sudo adduser $USER libvirtd
fi

#To check if qemu-kvm is installed
if [ $(dpkg-query -W -f='${Status}' qemu-kvm 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  sudo apt-get install qemu-kvm;
  echo "Install successful - qemu-kvm "
fi

#To install bridge-utils
if [ $(dpkg-query -W -f='${Status}' bridge-utils 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  sudo apt-get install bridge-utils;
  echo "Install successful - bridge utilities"
fi

# To install virtinst
if [ $(dpkg-query -W -f='${Status}' virtinst 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  sudo apt-get install virtinst;
  echo "Install successful - virstinst"
fi

# To install virt-viewer
if [ $(dpkg-query -W -f='${Status}' virt-viewer 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  sudo apt-get install virt-viewer;
  echo "Install successful - virt-manager"
fi

echo " Enter VM Name:"
read vm

echo " Enter RAM size in MB:"
read RAM

echo " Enter disk storage:"
read size1

echo "Number of CPU:"
read vcpu

echo "Enter OS Image Location"
read image

echo "Enter the number of interfaces"
read count

network=""
i=1

while [ $i -le $count ]
	do
		echo "Enter the name of your network:"
		read network
		isactive=$(sudo virsh net-info $network | grep Active: | awk '{print $2}')
		if [ "$active" == "no" ]
		then
			echo"Can not create VM. Network not active"
		else
			net_string=$net_string"--network network="$network" "
			echo net_string
			i=$(( $i + 1 ))
		fi
	done

echo "Installing VM....."

sudo virt-install -n ${vm} -r ${RAM} --vcpu=${vcpu} --cpu host --disk path=/var/lib/libvirt/images/$vm.ing,size=$size1 $net_string -c $image -v

echo "VM ${vm} Created"

sudo virsh list --all

#echo "To remove a VM entirely from the system"
#sudo virsh destroy $vm
#echo "VM is shutting down...."
#sudo virsh undefine $vm --remove-all-storage
#echo "VM deleted successfully"
