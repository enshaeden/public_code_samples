#!/bin/bash

if [ EUID -ne 0 ]
 then echo "Please run as root"
 exit 1
fi

BOOT_ID=$(lsblk | grep '/boot' | awk '{print $1}' | sed 's/└─//g' | sed 's/├─//g' | sed 's/p[0-9]//g' | head -n 1)
BOOT_DRIVE=$(lshw | grep $BOOT_ID | sed 's/logical name://g' | head -n 1 | awk '{print $1}')
CRYPT=$(dmsetup status | grep crypt | awk '{print $1}' | sed 's/p[0-9]_crypt://g')

chattr +d -Rf /home

dd if=/dev/urandom of=/home

case $CRYPT in
  $BOOT_DRIVE )
    dd if=/dev/urandom of=$BOOT_DRIVE bs=512 count=40960
    ;;
  * )
    dd if=/dev/urandom of=$BOOT_DRIVE bs=512
esac

