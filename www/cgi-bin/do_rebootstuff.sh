#!/bin/sh

# Version: 0.07 2014-10-07 SBP
#	Added echos for booting debugging purposes.

# Version: 0.06 2014-09-28 SBP
#	Added support for the HiFiBerry+ and IQaudIO+ cards. Improved the custom ALSA settings logic.

# Version: 0.05 2014-09-04 GE
#	Added cron-job variables and LMS auto-start variable.

# Version: 0.06 2014-09-09 GE
#	Added pcp_auto_start_lms at end of script.

# Version: 0.05 2014-09-04 GE
#	Added timezone function.

# Version: 0.04 2014-08-31 SBP
#	Minor formatting.

# Version: 0.03 2014-08-30 SBP
#	Clean up + added analog amixer use.
#	Improved the alsamixer use.

# Version: 0.02 2014-08-26 GE
#	Clean up.

# Version: 0.01 2014-06-25 SBP
#	Original.

echo "[ INFO ] Running do_rebootstuff.sh..."
echo "[ INFO ] Reading pcp-functions"
# Read from pcp-functions file
. /home/tc/www/cgi-bin/pcp-functions
pcp_variables
. $CONFIGCFG

echo "[ INFO ] Look at piCorePlayer.dep"
# Add eventual missing packages to onboot.lst. It is important if different versions of piCorePlayer have different needs.
# moved to do_update script, can be deleted if OK  
fgrep -vxf /mnt/mmcblk0p2/tce/onboot.lst /mnt/mmcblk0p2/tce/piCorePlayer.dep >> /mnt/mmcblk0p2/tce/onboot.lst

echo "[ INFO ] Checking for newconfig.cfg on sda1"
# Mount USB stick if present
# Check if sda1 is mounted otherwise mount it

MNTUSB=/mnt/sda1
if mount | grep $MNTUSB; then
	echo "mounted"
else
	echo "now trying to mount USB"
	sudo mount /dev/sda1
fi

# Check if newconfig.cfg is present
if [ -f $MNTUSB/newconfig.cfg ]; then
	sudo dos2unix -u $MNTUSB/newconfig.cfg

	# Read variables from newconfig and save to config.
	. $MNTUSB/newconfig.cfg

	# Save the parameters to the config file
	sudo sed -i "s/\(NAME=\).*/\1$NAME/" $CONFIGCFG
	sudo sed -i "s/\(OUTPUT=\).*/\1$OUTPUT/" $CONFIGCFG
	sudo sed -i "s/\(ALSA_PARAMS=\).*/\1$ALSA_PARAMS/" $CONFIGCFG
	sudo sed -i "s/\(BUFFER_SIZE=\).*/\1$BUFFER_SIZE/" $CONFIGCFG
	sudo sed -i "s/\(_CODEC=\).*/\1$_CODEC/" $CONFIGCFG
	sudo sed -i "s/\(PRIORITY=\).*/\1$PRIORITY/" $CONFIGCFG
	sudo sed -i "s/\(MAX_RATE=\).*/\1$MAX_RATE/" $CONFIGCFG
	sudo sed -i "s/\(UPSAMPLE=\).*/\1$UPSAMPLE/" $CONFIGCFG
	sudo sed -i "s/\(MAC_ADDRESS=\).*/\1$MAC_ADDRESS/" $CONFIGCFG
	sudo sed -i "s/\(SERVER_IP=\).*/\1$SERVER_IP/" $CONFIGCFG
	sudo sed -i "s/\(LOGLEVEL=\).*/\1$LOGLEVEL/" $CONFIGCFG
	sudo sed -i "s/\(LOGFILE=\).*/\1$LOGFILE/" $CONFIGCFG
	sudo sed -i "s/\(DSDOUT=\).*/\1$DSDOUT/" $CONFIGCFG
	sudo sed -i "s/\(VISULIZER=\).*/\1$VISULIZER/" $CONFIGCFG
	sudo sed -i "s/\(OTHER=\).*/\1$OTHER/" $CONFIGCFG
	sudo sed -i "s/\(AUDIO=\).*/\1$AUDIO/" $CONFIGCFG
	sudo sed -i "s/\(HOST=\).*/\1$HOST/" $CONFIGCFG
	sudo sed -i "s/\(SSID=\).*/\1$SSID/" $CONFIGCFG
	sudo sed -i "s/\(PASSWORD=\).*/\1$PASSWORD/" $CONFIGCFG
	sudo sed -i "s/\(ENCRYPTION=\).*/\1$ENCRYPTION/" $CONFIGCFG
	sudo sed -i "s/\(OVERCLOCK=\).*/\1$OVERCLOCK/" $CONFIGCFG
	sudo sed -i "s/\(CMD=\).*/\1$CMD/" $CONFIGCFG
	sudo sed -i "s/\(WIFI=\).*/\1$WIFI/" $CONFIGCFG
	sudo sed -i "s/\(FIQ=\).*/\1$FIQ/" $CONFIGCFG
	sudo sed -i "s/\(ALSAlevelout=\).*/\1$ALSAlevelout/" $CONFIGCFG
	sudo sed -i "s/\(TIMEZONE=\).*/\1$TIMEZONE/" $CONFIGCFG
	sudo sed -i "s/\(AUTOSTARTLMS=\).*/\1\"$AUTOSTARTLMS\"/" $CONFIGCFG
	sudo sed -i "s/\(REBOOT *=*\).*/\1$REBOOT/" $CONFIGCFG
	sudo sed -i "s/\(RB_H *=*\).*/\1$RB_H/" $CONFIGCFG
	sudo sed -i "s/\(RB_WD *=*\).*/\1$RB_WD/" $CONFIGCFG
	sudo sed -i "s/\(RB_DMONTH *=*\).*/\1$RB_DMONTH/" $CONFIGCFG
	sudo sed -i "s/\(RESTART *=*\).*/\1$RESTART/" $CONFIGCFG
	sudo sed -i "s/\(RS_H *=*\).*/\1$RS_H/" $CONFIGCFG
	sudo sed -i "s/\(RS_WD *=*\).*/\1$RS_WD/" $CONFIGCFG
	sudo sed -i "s/\(RS_DMONTH *=*\).*/\1$RS_DMONTH/" $CONFIGCFG
fi

# Rename the newconfig file on USB
if [ -f /mnt/sda1/newconfig.cfg ]; then sudo mv /mnt/sda1/newconfig.cfg /mnt/sda1/usedconfig.cfg; fi

echo "[ INFO ] Checking for newconfig.cfg on mmcblk0p1"
# Check if a newconfig.cfg file is present on mmcblk0p1 - requested by SqueezePlug and CommandorROR and used for insitu update
sudo mount /dev/mmcblk0p1
if [ -f /mnt/mmcblk0p1/newconfig.cfg ]; then
	sudo dos2unix -u /mnt/mmcblk0p1/newconfig.cfg

	# Read variables from newconfig and save to config.
	. /mnt/mmcblk0p1/newconfig.cfg

	# Save the parameters to the config file
	sudo sed -i "s/\(NAME=\).*/\1$NAME/" $CONFIGCFG
	sudo sed -i "s/\(OUTPUT=\).*/\1$OUTPUT/" $CONFIGCFG
	sudo sed -i "s/\(ALSA_PARAMS=\).*/\1$ALSA_PARAMS/" $CONFIGCFG
	sudo sed -i "s/\(BUFFER_SIZE=\).*/\1$BUFFER_SIZE/" $CONFIGCFG
	sudo sed -i "s/\(_CODEC=\).*/\1$_CODEC/" $CONFIGCFG
	sudo sed -i "s/\(PRIORITY=\).*/\1$PRIORITY/" $CONFIGCFG
	sudo sed -i "s/\(MAX_RATE=\).*/\1$MAX_RATE/" $CONFIGCFG
	sudo sed -i "s/\(UPSAMPLE=\).*/\1$UPSAMPLE/" $CONFIGCFG
	sudo sed -i "s/\(MAC_ADDRESS=\).*/\1$MAC_ADDRESS/" $CONFIGCFG
	sudo sed -i "s/\(SERVER_IP=\).*/\1$SERVER_IP/" $CONFIGCFG
	sudo sed -i "s/\(LOGLEVEL=\).*/\1$LOGLEVEL/" $CONFIGCFG
	sudo sed -i "s/\(LOGFILE=\).*/\1$LOGFILE/" $CONFIGCFG
	sudo sed -i "s/\(DSDOUT=\).*/\1$DSDOUT/" $CONFIGCFG
	sudo sed -i "s/\(VISULIZER=\).*/\1$VISULIZER/" $CONFIGCFG
	sudo sed -i "s/\(OTHER=\).*/\1$OTHER/" $CONFIGCFG
	sudo sed -i "s/\(AUDIO=\).*/\1$AUDIO/" $CONFIGCFG
	sudo sed -i "s/\(HOST=\).*/\1$HOST/" $CONFIGCFG
	sudo sed -i "s/\(SSID=\).*/\1$SSID/" $CONFIGCFG
	sudo sed -i "s/\(PASSWORD=\).*/\1$PASSWORD/" $CONFIGCFG
	sudo sed -i "s/\(ENCRYPTION=\).*/\1$ENCRYPTION/" $CONFIGCFG
	sudo sed -i "s/\(OVERCLOCK=\).*/\1$OVERCLOCK/" $CONFIGCFG
	sudo sed -i "s/\(CMD=\).*/\1$CMD/" $CONFIGCFG
	sudo sed -i "s/\(WIFI=\).*/\1$WIFI/" $CONFIGCFG
	sudo sed -i "s/\(FIQ=\).*/\1$FIQ/" $CONFIGCFG
	sudo sed -i "s/\(ALSAlevelout=\).*/\1$ALSAlevelout/" $CONFIGCFG
	sudo sed -i "s/\(TIMEZONE=\).*/\1$TIMEZONE/" $CONFIGCFG
	sudo sed -i "s/\(AUTOSTARTLMS=\).*/\1\"$AUTOSTARTLMS\"/" $CONFIGCFG
	sudo sed -i "s/\(REBOOT *=*\).*/\1$REBOOT/" $CONFIGCFG
	sudo sed -i "s/\(RB_H *=*\).*/\1$RB_H/" $CONFIGCFG
	sudo sed -i "s/\(RB_WD *=*\).*/\1$RB_WD/" $CONFIGCFG
	sudo sed -i "s/\(RB_DMONTH *=*\).*/\1$RB_DMONTH/" $CONFIGCFG
	sudo sed -i "s/\(RESTART *=*\).*/\1$RESTART/" $CONFIGCFG
	sudo sed -i "s/\(RS_H *=*\).*/\1$RS_H/" $CONFIGCFG
	sudo sed -i "s/\(RS_WD *=*\).*/\1$RS_WD/" $CONFIGCFG
	sudo sed -i "s/\(RS_DMONTH *=*\).*/\1$RS_DMONTH/" $CONFIGCFG
fi

# Save changes caused by the presence of a newconfig.cfg file
if [ -f /mnt/mmcblk0p1/newconfig.cfg ]; then sudo filetool.sh -b; fi
# Delete the newconfig file
sudo rm -f /mnt/mmcblk0p1/newconfig.cfg
sleep 1
sudo umount /mnt/mmcblk0p1

#Section to save the parameters to the wifi.db - this is a new version in order to saving space and backslash in SSID which is needed in wifi.db
# so a name like "steens wifi" should be saved as  "steens\ wifi"
echo "[ INFO ] Reading config.cfg"
. /usr/local/sbin/config.cfg

#sudo chmod 766 /home/tc/wifi.db
#Only add backslash if not empty
echo "[ INFO ] Updating wifi.db"
if [ X"" = X"$SSID" ]; then break
else SSSID=`echo "$SSID" | sed 's/\ /\\\ /g'`
#Change SSSID back to SSID
SSID=$SSSID
sudo echo ${SSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION}> /home/tc/wifi.db
pcp_backup_nohtml
fi

# We do have a problem with SSID's which don't have a name - should we use the next section for these SSIDs - I have not tested the code
# Saves SSID if empty
# if [ X"" = X"$SSID" ]; then sudo chmod 766 /home/tc/wifi.db; sudo echo ${SSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION}> /home/tc/wifi.db; else fi
# NEW Section ends here

# Save changes caused by the presence of a newconfig.cfg file and wifi copy from config.cfg to wifi.db fie
# Is already save - I think - sudo filetool.sh -b

# Stuff previously handled by bootlocal.sh - but sits better here allowing for in situ update of as bootlocal then can be kept free from piCorePlayer stuff
# allowing any custom changes to bootlocal.sh to be maintained as it is not overwritten by in situ update.

echo "[ INFO ] Loading snd modules" 
sudo modprobe snd-bcm2835
#sudo modprobe -r snd_soc_wm8731
sudo modprobe snd_soc_bcm2708_i2s
sudo modprobe bcm2708_dmaengine
sudo modprobe snd_soc_wm8804

#Read from config file.
. $CONFIGCFG

echo "[ INFO ] Checking wifi is ON?"
# Logic that will skip the wifi connection if wifi is disabled
if [ $WIFI = on ]; then 
	sudo ifconfig wlan0 down
	sleep 1
	sudo ifconfig wlan0 up
	sleep 1
	sudo iwconfig wlan0 power off &>/dev/null
	sleep 1
	#usr/local/bin/wifi.sh -a 2>&1 > /tmp/wifi.log
	usr/local/bin/wifi.sh -a
	sleep 1

	# Logic that will try to reconnect to wifi if failed - will try two times before continuing booting
	for i in 1 2; do
		if ifconfig wlan0 | grep -q "inet addr:" ; then
			echo "connected"      
		else
			echo "Network connection down! Attempting reconnection two times before continuing."
			sudo ifconfig wlan0 down
			sleep 1
			sudo ifconfig wlan0 up
			sleep 1
			sudo iwconfig wlan0 power off &>/dev/null
			sleep 1
			sudo /usr/local/bin/wifi.sh -a
			sleep 10
	   fi
	done
fi

# New section using Gregs functions, Remove all I2S stuff and load the correct modules

echo "[ INFO ] Loading I2S modules"

if [ $AUDIO = HDMI ]; then sudo $pCPHOME/enablehdmi.sh; else sudo $pCPHOME/disablehdmi.sh; fi

sleep 5

if [ $AUDIO = Analog ]; then pcp_disable_i2s; else break; fi
if [ $AUDIO = USB ]; then pcp_disable_i2s; else break; fi
if [ $AUDIO = I2SDAC ]; then pcp_enable_i2s_dac; else break; fi
if [ $AUDIO = I2SDIG ]; then pcp_enable_i2s_digi; else break; fi
if [ $AUDIO = I2SpDAC ]; then pcp_enable_hifiberry_dac_p; else break; fi
if [ $AUDIO = I2SpDIG ]; then pcp_enable_i2s_digi; else break; fi
if [ $AUDIO = I2SpIQaudIO ]; then pcp_enable_iqaudio_dac; else break; fi
if [ $AUDIO = IQaudio ]; then pcp_enable_iqaudio_dac; else break; fi

# Sleep for 1 sec otherwise aplay can not see the card
sleep 1
# Check for onboard sound card is card=0, so amixer is only used here
echo "[ INFO ] Doing ALSA configuration"
aplay -l | grep 'card 0: ALSA' &> /dev/null
if [ $? == 0 ] && [ $AUDIO = Analog ]; then
	if [ $ALSAlevelout = Default ]; then
		sudo amixer set PCM 400 unmute
	fi
fi

# If Custom ALSA settings are used, then restore the settings
if [ $ALSAlevelout = Custom ]; then
	alsactl restore
fi

# Start the essential stuff for piCorePlayer

echo "[ INFO ] Loading the main daemons"
echo -n "[ INFO ] "
/usr/local/etc/init.d/dropbear start
echo -n "[ INFO ] "
/usr/local/etc/init.d/httpd start
sleep 1
echo -n "[ INFO ] "
/usr/local/etc/init.d/squeezelite start

# Only call timezone function if timezone variable is set
if [ X"" != X"$TIMEZONE" ]; then
	echo "[ INFO ] Setting timezone"
	pcp_set_timezone
fi

echo "[ INFO ] Doing auto start LMS"
pcp_auto_start_lms
