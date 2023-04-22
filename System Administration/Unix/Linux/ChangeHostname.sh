#!/bin/bash

if [[ $EUID -ne 0 ]]
	echo "Please run as root"
	exit 1
fi

# uncomment to change host name based on logged in user name
#sed '/127.0.1.1/s/[a-z]*$/'$LOGNAME'-dev/' /etc/hosts
#sed 's/[a-z]*/'$LOGNAME'-dev/g' /etc/hostname

# change hostname based on read input
declare -l hostname
read -p 'Enter username (jappleseed) > ' $hostname
sed '/127.0.1.1/s/[a-z]*$/'$hostname'-dev/' /etc/hosts
sed 's/[a-z]*/'$hostname'/g' /etc/hostname

