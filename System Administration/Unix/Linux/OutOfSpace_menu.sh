#!/bin/bash
# This script is designed to make an easier time of
# finding out where all the disk usage has gone to
# when a user reports that their boot drive is full

# check if run as root or sudo
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

while [[ "$REPLY" != 0 ]]; do
  clear
  cat <<- _EOF_
    Please select:

    1) Display System Information
    2) Display Disk Space
    3) Display Home Folder Utilization
    0) Quit

_EOF_
read -p "Enter selection (0-3) > "

case $REPLY in
  0 ) # Exit
    echo "Thank you!"
    exit 0
      ;;
  1 ) #sytem information
    echo "Hostname: $HOSTNAME"
    uptime
    sleep 2
    continue
      ;;
  2 ) # Disk Space
    # get physical disk where boot partition resides
    DISK_ID=$(fdisk -l | grep '^/dev/[a-z]*[0-9]' | awk '{print $1}' | sed 's/p[0-9]//g' | head -n 1)
    # check disk usage of the boot drive and print simplified output
    echo "These are the current stats for your computer's storage."
    df -h $DISK_ID | awk '{print $1, $3, $4, $5}'
    read -p "Continue? (y/n) >" RETURN
    case $RETURN in
      y|yes|Y|Yes|YES )
        continue
          ;;
      n|no|N|No|NO )
        break
          ;;
      * )
        echo "Invalid selection, please enter (Y)es or (N)o."
        sleep 1
        exec "$0" "$@"
          ;;
    esac
      ;;
  3 ) # Home Folder Utilization
    # find user HomeFolder
    read -p "What is your username? > " HomeFolder
    # check disk usage by home folder and print simplified output
    echo "This is the curent allocation of data in your home folder"
    df -h /home/$HomeFolder | awk '{print $1, $3, $4, $5}'
    sleep 1
    echo "Would you like to refine your search?"
    read -p '(y/n)' Continue
    if [[ ! $Continue =~(y|yes|Y|Yes|n|no|N|No)$ ]]; then
      echo "Invalid selection, please enter (Y)es or (N)o."
      sleep 1
      exec "$0" "$@"
    fi
    case $Continue in
      y|yes|Y|Yes|1 )
        # check disk usage by file size
          echo "What is the smallest file size you wish to see?"
          echo "examples include 10k | 1000M | 10G"
          read -p '>' FileSize
          echo "These are the top 10 largest files in /home/$HomeFolder."
          du -h -t $FileSize /home/$HomeFolder | sort -n | head | sort -r
            ;;
      n|no|N|No|2 )
        clear
        exit 0
            ;;
    esac
      ;;
esac

done