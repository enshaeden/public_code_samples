
#!/bin/bash
#This is a simple script to disable the user ability to access the GRUB at boot
#this will prevent unwanted access to root level pre-boot tools to modify users and core files

#uncomment to enable Root check
if [ $EUID -ne 0 ]
  then echo "Please run as root"
  exit
fi

#appends line to default GRUB file and runs the update-grub command to apply the change on reboot
sed -i '/GRUB_DISABLE_RECOVERY/s/^#//' /etc/default/grub && update-grub
