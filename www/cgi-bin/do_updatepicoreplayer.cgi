#!/bin/sh

# Version: 0.09 2015-05-21 SBP
#	Save custom ALSA settings.

# Version: 0.08 2014-12-11 GE
#	HTML5 formatting.

# Version: 0.07 2014-10-01 GE
#	Added  class="error" to error messages.
#	Added check for free space before untarring.

# Version: 0.06 2014-09-05 GE
#	Added INSITU_DOWNLOAD variable.

# Version: 0.05 2014-08-23 SBP
#	Added function so that onboot.lst will not be overwritten.
#	Added function so that new needed packages for piCorePlayer will be added to onboot.lst from list in the new piCorePlayer home.

# Version: 0.04 2014-07-19 GE
#	Improved error checking.
#	Added pcp_go_main_button and pcp_navigation.

# Version: 0.03 2014-07-13 SBP
#	Added command to remove kernel specific files in the optional directory.

# Version: 0.02 2014-06-24 GE
#	Rewritten.

# Version: 0.01 2014 SBP
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

# Read the version from the temp file
. $UPD_PCP/version.cfg

pcp_html_head "Update pCP" "SBP"

pcp_banner
pcp_navigation
pcp_running_script

#=========================================================================================
# Check for sufficient free space to untar to partition mmcblk0p2
#-----------------------------------------------------------------------------------------
FREE_SPACE=$(df | grep mmcblk0p2 | awk '{ print ($2-$3) }')
TAR_FILE_SIZE=$(ls -s "$UPD_PCP"/tce/"$INSITU"_tce.tar.gz | awk '{ print $1 }')
CONTINUE=`expr $FREE_SPACE - $TAR_FILE_SIZE`

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] free space on mmcblk0p2: '$FREE_SPACE'<br />'
	echo '                 [ DEBUG ] file size              : '$TAR_FILE_SIZE'<br />'
	echo '                 [ DEBUG ] Continue               : '$CONTINUE'</p>'

	if [ $CONTINUE -lt 0 ]; then
		echo '<p class="error">[ ERROR ] Not enough free space on mmcblk0p2</p>'
		pcp_go_main_button
		echo '</body>'
		echo '</html>'
		exit
	fi
	echo '<p>Continue</p>'
fi
#-----------------------------------------------------------------------------------------

pcp_mount_mmcblk0p1

# Delete all files from the boot partition
sudo rm -rf /mnt/mmcblk0p1/* 

#=========================================================================================
# Copy ALSA settings so they are avaiable after an update
#-----------------------------------------------------------------------------------------
if [ ALSAlevelout="Custom" ]; then
sudo cp /etc/asound.conf /mnt/mmcblk0p1/
sudo cp /var/lib/alsa/asound.state /mnt/mmcblk0p1/
fi
#-----------------------------------------------------------------------------------------


# Copy the config file to boot partition
sudo cp -f /usr/local/sbin/config.cfg /mnt/mmcblk0p1/newconfig.cfg 
sudo dos2unix -u /mnt/mmcblk0p1/newconfig.cfg
echo '<p class="info">[ INFO ] Your config has been saved so your current settings will used be after updating piCorePlayer.</p>'

# Untar and overwrite the boot files
echo '<p class="info">[ INFO ] Untarring '$INSITU'_boot.tar.gz...</p>'
echo '<textarea name="TextBox" cols="120" rows="8">'
sudo tar -zxvf $UPD_PCP/boot/"$INSITU"_boot.tar.gz -C /
result_boot=$?
echo '</textarea>'

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] boot tar result: '$result_boot'</p>'

pcp_umount_mmcblk0p1

if [ $result_boot = 0 ]; then
	# Delete all the kernel specific files in the optional directory - so no stray files are left
	sudo rm -rf /mnt/mmcblk0p2/tce/optional/*piCore*.*

	# Untar and overwrite the tce files
	echo '<p class="info">[ INFO ] Untarring '$INSITU'_tce.tar.gz...</p>'
	echo '<textarea name="TextBox" cols="120" rows="8">'
	sudo tar -zxvf $UPD_PCP/tce/"$INSITU"_tce.tar.gz -C /
	result_tce=$?
	echo '</textarea>'

	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] tce tar result: '$result_tce'</p>'

	if [ $result_tce = 0 ]; then
		echo '<h2>[ INFO ] piCorePlayer has been updated, please reboot now. And then you should have: '$INSITU'</h2>'
		pcp_reboot_button
	else
		echo '<p class="error">[ ERROR ] piCorePlayer has NOT been updated.</p>'
	fi
else
	echo '<p class="error">[ ERROR ] piCorePlayer has NOT been updated.</p>'
fi

# Add eventual missing packages to onboot.lst. It is important if different versions of piCorePlayer have different needs.
fgrep -vxf /mnt/mmcblk0p2/tce/onboot.lst /mnt/mmcblk0p2/tce/piCorePlayer.dep >> /mnt/mmcblk0p2/tce/onboot.lst

#Remove wifi firmware from onboot.lst if wifi is off so that pCP will boot faster
if [ $WIFI = off ]; then
sleep 1
	sudo sed -i '/firmware-ralinkwifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/firmware-rtlwifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/firmware-atheros.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/wireless/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/wifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
fi

pcp_go_main_button

echo '</body>'
echo '</html>'