#!/bin/sh

# Version: 7.0.0 2020-06-08

. pcp-functions
. pcp-soundcard-functions  # reset needs soundcard functions too.

# Restore sparams variable value from pcp.cfg so it is not overwritten with default values
PARAM1="$SPARAMS1"
PARAM2="$SPARAMS2"
PARAM3="$SPARAMS3"
PARAM4="$SPARAMS4"
PARAM5="$SPARAMS5"

# Read original mmap value, so we only do something if value is changed
ORG_ALSA_PARAMS4=$(echo $ALSA_PARAMS | cut -d':' -f4 )

RESTART_REQUIRED=TRUE
unset REBOOT_REQUIRED

pcp_html_head "Write to pcp.cfg" "SBP" "15" "squeezelite.cgi"

pcp_navbar
pcp_remove_query_string
pcp_httpd_query_string

#========================================================================================
# Reset configuration
#----------------------------------------------------------------------------------------
pcp_reset() {
	pcp_reset_config_to_defaults
}

#========================================================================================
# Restore configuration
#
# Note: Assumes a backup onto USB stick exists.
#----------------------------------------------------------------------------------------
pcp_restore() {
	pcp_mount_device sda1
	. /mnt/sda1/newpcp.cfg
	pcp_umount_device sda1
	pcp_save_to_config
}

#========================================================================================
# Update pcp.cfg to the latest version
#
# This will first create the latest version of pcp.cfg with default values, then,
# restore original values.
#----------------------------------------------------------------------------------------
pcp_update() {
	pcp_message INFO "Copying pcp.cfg to /tmp..." "text"
	sudo cp $PCPCFG /tmp/pcp.cfg
	[ $? -ne 0 ] && pcp_message ERROR "Error copying pcp.cfg to /tmp..." "text"
	pcp_message INFO "Setting pcp.cfg to defaults..." "text"
	pcp_update_config_to_defaults
	pcp_message INFO "Updating pcp.cfg with original values..." "text"
	. $PCPCFG
	. /tmp/pcp.cfg
	pcp_save_to_config
}

#========================================================================================
# Shutdown monitor
#----------------------------------------------------------------------------------------
install_shutdown_monitor() {
	if [ ! -f $PACKAGEDIR/shutdown-monitor.tcz ]; then
		echo "Installing Shutdown Monitor"
		sudo -u tc pcp-load -r $PCP_REPO -w shutdown-monitor.tcz
		if -f $PACKAGEDIR/shutdown-monitor.tcz ]; then
			sudo -u tc pcp-load -i shutdown-monitor.tcz
			echo "shutdown-monitor.tcz" >> $ONBOOTLST
		fi
	else
		sed -i '/shutdown-monitor.tcz/d' $ONBOOTLST
		echo "shutdown-monitor.tcz" >> $ONBOOTLST
		sudo -u tc pcp-load -i shutdown-monitor.tcz
	fi
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_heading5 "Write to config"

case "$SUBMIT" in
	Save)
		if [ $MODE -ge $MODE_PLAYER ]; then
			ALSA_PARAMS=${ALSA_PARAMS1}:${ALSA_PARAMS2}:${ALSA_PARAMS3}:${ALSA_PARAMS4}:${ALSA_PARAMS5}
			[ $CLOSEOUT -eq 0 ] && CLOSEOUT=""
			[ $PRIORITY -eq 0 ] && PRIORITY=""
			[ $POWER_GPIO -eq 0 ] && POWER_GPIO=""
		fi
		[ $SQUEEZELITE = "no" ] && unset RESTART_REQUIRED
		pcp_infobox_begin
		pcp_message INFO "Saving config file." "text"
		pcp_save_to_config
		pcp_footer static >/tmp/footer.html
		pcp_backup "text"
		pcp_infobox_end
	;;
	Binary)
		SAVE=0
		case $SQBINARY in
			default)
				rm -f $TCEMNT/tce/squeezelite
				SAVE=1
			;;
			custom)
				if [ -f $TCEMNT/tce/squeezelite-custom ]; then
					rm -f $TCEMNT/tce/squeezelite
					ln -s $TCEMNT/tce/squeezelite-custom $TCEMNT/tce/squeezelite
					SAVE=1
				else
					pcp_infobox_begin
					pcp_message ERROR "Custom Squeezelite not found. Copy custom binary before setting this option." "html"
					pcp_infobox_end
				fi
			;;
		esac
		if [ $SAVE -eq 1 ]; then
			pcp_infobox_begin
			pcp_message INFO "Saving Squeezelite to $SQBINARY." "text"
			pcp_message INFO "Saving config file." "text"
			pcp_save_to_config
			pcp_backup "text"
			pcp_infobox_end
		fi
	;;
	Reset*)
		pcp_reset
	;;
	Restore*)
		pcp_restore
	;;
	Update*)
		pcp_update
	;;
	Poweroff)
		unset RESTART_REQUIRED
		REBOOT_REQUIRED=1
		case $GPIOPOWEROFF in
			yes)
				pcp_mount_bootpart
				sed -i '/dtoverlay=gpio-poweroff/d' $CONFIGTXT
				[ $GPIOPOWEROFF_HI = "yes" ] && ACTIVELOW="" || ACTIVELOW=",active_low=1"
				echo "dtoverlay=gpio-poweroff,gpiopin=${GPIOPOWEROFF_GPIO}${ACTIVELOW}" >> $CONFIGTXT
				pcp_umount_bootpart
			;;
			no)
				pcp_mount_bootpart
				sed -i '/dtoverlay=gpio-poweroff/d' $CONFIGTXT
				pcp_umount_bootpart
			;;
		esac
		pcp_save_to_config
	;;
	Shutdown)
		unset RESTART_REQUIRED
		REBOOT_REQUIRED=1
		case $GPIOSHUTDOWN in
			yes)
				pcp_mount_bootpart
				sed -i '/dtoverlay=gpio-shutdown/d' $CONFIGTXT
				[ $GPIOSHUTDOWN_HI = "yes" ] && ACTIVELOW="active_low=0" || ACTIVELOW="active_low=1"
				echo "dtoverlay=gpio-shutdown,gpio_pin=${GPIOSHUTDOWN_GPIO},${ACTIVELOW},gpio_pull=${GPIOSHUTDOWN_PU}" >> $CONFIGTXT
				pcp_umount_bootpart
				install_shutdown_monitor
			;;
			no)
				pcp_mount_bootpart
				sed -i '/dtoverlay=gpio-shutdown/d' $CONFIGTXT
				pcp_umount_bootpart
				sed -i '/shutdown-monitor.tcz/d' $ONBOOTLST
			;;
		esac
		pcp_save_to_config
	;;
	Install-monitor)
		unset RESTART_REQUIRED
		install_shutdown_monitor
	;;
	*)
		pcp_message ERROR "Invalid case argument." "text"
	;;
esac

. $PCPCFG

if [ "$ALSAeq" = "yes" ] && [ "$OUTPUT" != "equal" ]; then
	STRING1='ALSA equalizer is enabled. In order to use it "equal" must be used in the OUTPUT box. Press [OK] to go back and change or [Cancel] to continue'
	SCRIPT1=squeezelite.cgi
	pcp_confirmation_required
fi

#pcp_backup   # <===== GE Eventually remove this

[ $RESTART_REQUIRED ] || pcp_redirect_button "Go Back" $FROM_PAGE 5

pcp_footer
pcp_copyright

sleep 1
[ $REBOOT_REQUIRED ] && pcp_reboot_required
[ $RESTART_REQUIRED ] && pcp_restart_required $FROM_PAGE   # <===== GE Eventually remove this

echo '</div>'
echo '</body>'
echo '</html>'
