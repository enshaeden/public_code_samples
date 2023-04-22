#!/bin/zsh

/bin/cat << EOF > /usr/local/Scripts/file_cleanup.py

import os
import shutil
from datetime import datetime


def convert_epoch_to_y_m(epoch_time):
    file_date = datetime.fromtimestamp(epoch_time)
    formatted_date = file_date.strftime('%Y-%m')
    return formatted_date


class FileInfo:
    def __init__(self, file_stats):
        self.file_links = file_stats.st_nlink
        self.file_size = file_stats.st_size
        self.file_modified = convert_epoch_to_y_m(file_stats.st_mtime)
        self.file_uid = file_stats.st_uid
        self.file_gid = file_stats.st_gid
        self.file_permissions = file_stats.st_mode
        self.file_inode = file_stats.st_ino
        self.inode_device = file_stats.st_dev
        self.date_of_last_access = file_stats.st_atime
        self.date_of_last_change = file_stats.st_ctime
        self.birthdate = convert_epoch_to_y_m(file_stats.st_birthtime)


def get_list_of_dates(folder):
    dates = {}
    for file in os.listdir(folder):
        file_stats = os.stat(f"{folder}/{file}")
        file_info = FileInfo(file_stats)
        date = file_info.birthdate
        
        date_year = date[:4]
        date_month = date[5:7]

        if date_year not in dates:
            dates[date_year] = []
        if date_month not in dates[date_year]:
            dates[date_year].append(date_month)
    return dates


def make_folders(dates, path):
    for year in dates:
        year_path = f"{path}/{year}"
        if not os.path.exists(year_path):
            os.mkdir(year_path)
        for month in dates[year]:
            month_path = f"{year_path}/{month}"
            if not os.path.exists(month_path):
                os.mkdir(month_path)


def file_cleanup(folder):
    # create a list of dates based on the birthdate of the files
    # create folders for each year and each month
    dates = get_list_of_dates(folder)
    make_folders(dates, folder)

    for file in os.listdir(folder):
        # generate file info object
        file_stats = os.stat(f"{folder}/{file}")
        file_info = FileInfo(file_stats)

        # if file is not a directory
        if file_info.file_links <= 1 or file_info.file_permissions != 16877:
            # check creation date
            file_created = file_info.birthdate
            file_created_year = file_created[:4]
            file_created_month = file_created[5:7]

            # look for matching year folder
            for file2 in os.listdir(folder):
                if file_created_year == file2:
                    year_path = f"{folder}/{file2}"

                    # look for matching month folder
                    for file3 in os.listdir(year_path):
                        if file_created_month == file3:
                            # move file to month folder in appropriate year folder
                            shutil.move(f"{folder}/{file}", f"{year_path}/{file3}")
                        

if __name__ == '__main__':
    user_home = os.path.expanduser('~')     # get user home directory
    desktop_folder = f"{user_home}/Desktop"
    downloads_folder = f"{user_home}/Downloads"

    file_cleanup(desktop_folder)
    file_cleanup(downloads_folder)

EOF

# Write the LaunchDaemon
/bin/cat << EOF > /Library/LaunchAgents/net.enshaeden.file_cleanup.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>net.enshaeden.file_cleanup</string>
	<key>ProgramArguments</key>
	<array>
        <string>/usr/local/bin/python3</string>
		<string>/usr/local/Scripts/file_cleanup.py</string>
	</array>
	<key>StartInterval</key>
    <integer>5760</integer>
</dict>
</plist>
EOF

/bin/chmod 644 /Library/LaunchAgents/net.enshaeden.file_cleanup.plist
/usr/sbin/chown root:wheel /Library/LaunchAgents/net.enshaeden.file_cleanup.plist
/bin/launchctl bootstrap -w /Library/LaunchAgents/net.enshaeden.file_cleanup.plist
