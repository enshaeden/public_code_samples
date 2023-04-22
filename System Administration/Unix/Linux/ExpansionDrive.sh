#!/bin/bash

if [ $EUID -ne 0 ]
   then echo "Please run as root"
   exit
fi

DISK_ID=$(fdisk -l | grep '^/dev/sd[a-z]*[0-9]' | awk '{print $1}' |sed 's/[0-9]//g' | head -n 1)
VOLUME_GROUP="/dev/$(vgdisplay |grep 'VG Name' | awk  '{print $3}' | head -n 1)"
LOGICAL_VOLUME=$(lvdisplay | grep '^/dev/[a-z]*[0-9]' | awk '{print $1}' | tail -n 1 | grep -Eo '[0-9]+$')
NEW_PARTITION=$(($(echo $END_PARTITION | grep -Eo '[0-9]+$')+1))

case $DISK_ID in
    /dev/sd*)
	;;
    *) echo "could not identify sdX class disk"
	exit 1
		;;
esac

sed -e 's/\s*\([\+0-9a-zA-Z]*\).*/\1/' << EOF | fdisk ${DISK_ID}
 d #
   #
 d #
   #
 d #
   #
 d #
   #
 n #
 1 #
   #
   #
 t #
 30#
 w #
 q #
EOF

pvcreate -ff "$DISK_ID""$NEW_PARTITION"

vgextend "$VOLUME_GROUP" "$DISK_ID""$NEW_PARTITION"

lvextend "$LOGICAL_VOLUME" "$DISK_ID""$NEW_PARTITION"

resize2fs "$LOGICAL_VOLUME"

