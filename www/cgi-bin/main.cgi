#!/bin/sh

# Version: 0.20 2016-02-03 GE
#	Changed Insitu update.

# Version: 0.19 2016-01-15 GE
#	Updated "Update pCP" help text.

# Version: 0.18 2016-01-07 GE
#	Added check for version of Ralphy's squeezelite.
#	Added Shairport indicator and restart option.

# Version: 0.17 2015-12-09 SBP
#	Removed Update Triode's version of Squeezelite.
#	Updated download and update Ralphy's version of Squeezelite.

# Version: 0.16 2015-09-20 GE
#	Added fieldsets around Advanced, Beta and Developer modes.
#	Fixed pcp_main_reset_all routine.

# Version: 0.15 2015-08-29 GE
#	Revised modes.
#	Turned pcp_picoreplayers tabs on in normal mode.
#	Changed reboot, shutdown and backup messages.
#	Added warning message on reset all.

# Version: 0.14 2015-07-01 GE
#	Added pcp_mode tabs.
#	Added pcp_picoreplayers tabs.
#	Removed some unnecessary code.

# Version: 0.13 2015-05-11 GE
#	Now uses pcp_start_row_shade, pcp_start_row_shade and pcp_incr_id
#	Added Extensions, Extras, Debug and Diagnostics buttons.
#	Added Static IP to Main piCorePlayer operations.

# Version: 0.12 2015-02-20 GE
#	Moved Disable GUI, Stop Squeezelite, Backup and Shutdown to Developers operations.
#	Added Reset ALL and Restore ALL to Developers operations.

# Version: 0.11 2015-01-26 SBP
#	Added Disable GUI.

# Version: 0.10 2014-12-20 GE
#	Modified Squeezelite running indicator.

# Version: 0.09 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.08 2014-12-08 SBP
#	Revised button order.
#	Added Squeezelite running indicator.
#	Reformatted.

# Version: 0.07 2014-10-22 GE
#	Using pcp_html_head now.

# Version: 0.06 2014-10-09 GE
#	Revised uptime delay to use seconds.

# Version: 0.05 2014-10-08 GE
#	Size of input buttons controlled through input[type=submit] style.

# Version: 0.04 2014-10-02 GE
#	Added uptime delay before pcp_squeezelite_status is checked.

# Version: 0.03 2014-09-20 GE
#	Modified HTML to improve cross browser support.

# Version: 0.02 2014-08-22 GE
#	Added check for pcp_squeezelite_status.

# Version: 0.01 2014-06-25 GE
#	Original.

. pcp-lms-functions
. pcp-functions
pcp_variables

pcp_html_head "Main Page" "SBP"

[ $MODE -ge $MODE_NORMAL ] && pcp_picoreplayers
[ $MODE -ge $MODE_ADVANCED ] && pcp_controls
pcp_banner
pcp_navigation

#========================================================================================
# Main piCorePlayer operations
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Main piCorePlayer operations</legend>'
echo '          <table class="bggrey percent100">'

#------------------------------------Squeezelite/Shairport Indication--------------------
pcp_main_squeezelite_indication() {

	if [ $(pcp_squeezelite_status) = 0 ]; then
		IMAGE="green.png"
		STATUS="running"
	else
		IMAGE="red.png"
		STATUS="not running"
	fi

	pcp_start_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150">'
	echo '                <p class="centre"><img src="../images/'$IMAGE'" alt="'$STATUS'"></p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Squeezelite is '$STATUS'&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <ul>'
	echo '                    <li>GREEN = Squeezelite running.</li>'
	echo '                    <li>RED = Squeezelite not running.</li>'
	echo '                  </ul>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Squeezelite must be running for music to play.</li>'
	echo '                    <li>Squeezelite must be running for connection to LMS.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'

	if [ $SHAIRPORT = yes ]; then

		if [ $(pcp_shairport_status) = 0 ]; then
			SH_IMAGE="green.png"
			SH_STATUS="running"
		else
			SH_IMAGE="red.png"
			SH_STATUS="not running"
		fi

		pcp_incr_id
		echo '            <tr class="'$ROWSHADE'">'
		echo '              <td class="column150">'
		echo '                <p class="centre"><img src="../images/'$SH_IMAGE'" alt="'$SH_STATUS'"></p>'
		echo '              </td>'
		echo '              <td>'
		echo '                <p>Shairport is '$SH_STATUS'&nbsp;&nbsp;'
		echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                </p>'
		echo '                <div id="'$ID'" class="less">'
		echo '                  <ul>'
		echo '                    <li>GREEN = Shairport running.</li>'
		echo '                    <li>RED = Shairport not running.</li>'
		echo '                  </ul>'
		echo '                  <p><b>Note:</b></p>'
		echo '                  <ul>'
		echo '                    <li>Shairport must be running for music to play from iDevices.</li>'
		echo '                  </ul>'
		echo '                </div>'
		echo '              </td>'
		echo '            </tr>'
	fi
}
pcp_main_squeezelite_indication
#----------------------------------------------------------------------------------------

#------------------------------------------Padding---------------------------------------
pcp_main_padding() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="padding '$ROWSHADE'">'
	echo '              <td></td>'
	echo '              <td></td>'
	echo '            </tr>'
}
pcp_main_padding
#----------------------------------------------------------------------------------------

#-------------------------------Restart - Squeezelite / Shairpoint-----------------------
pcp_main_restart_squeezelite() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Restart" action="restartsqlt.cgi" method="get">'
	echo '                  <input type="submit" value="Restart" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Restart Squeezelite with new settings&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will kill the Squeezelite process then restart it.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>A restart of Squeezelite is required after you change any of the Squeezelite settings.</li>'
	echo '                    <li>Squeezelite running indicator will turn green.</li>'
	echo '                    <li>Squeezelite in the footer will turn green.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}

pcp_main_restart_shairport() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Restart" action="restartsqlt.cgi" method="get">'
	echo '                  <input type="submit" value="Restart" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Restart Squeezelite and Shairport with new settings&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will kill the Squeezelite and Shairport processes then restart them.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>A restart of Squeezelite and Shairport is required after you change any of the Squeezelite settings.</li>'
	echo '                    <li>Squeezelite and Shairport running indicators will turn green.</li>'
	echo '                    <li>Squeezelite in the footer will turn green.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $SHAIRPORT = yes ] && pcp_main_restart_shairport || pcp_main_restart_squeezelite
#----------------------------------------------------------------------------------------

#------------------------------------------Padding---------------------------------------
[ $MODE -le $MODE_BASIC ] && pcp_main_padding
#----------------------------------------------------------------------------------------

#------------------------------------------Update Squeezelite - Ralphy-------------------
pcp_main_update_ralphy() {

	SIZE=$(ls -l /mnt/mmcblk0p2/tce/squeezelite-armv6hf | awk '{ print $5 }')
	if [ $SIZE -lt 2000000 ]; then
		VERSIONsmall="selected"
	else
		VERSIONlarge="selected"
	fi

	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <form name="updateRalphys" action="updatesqlt.cgi" method="get">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <select class="large16" name="VERSION">'
	echo '                    <option value="Small" '$VERSIONsmall'>Ralphy'\''s basic version</option>'
	echo '                    <option value="Large" '$VERSIONlarge'>Ralphy'\''s ffmpeg version</option>'
	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Select and update Squeezelite&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will download and install Squeezelite from Ralphy'\''s repository.</p>'
	echo '                    <p><b>Note:</b></p>'
	echo '                    <ul>'
	echo '                      <li>Internet access is required.</li>'
	echo '                      <li>The basic version is 1MB which plays pcm, (wav/aiff), flac, mp3, ogg and aac.</li>'
	echo '                      <li>The ffmpeg version is 12MB which in addition plays ALAC and WMA (ffmpeg is built in).</li>'
	echo '                      <li>Triode is the original author of Squeezelite.</li>'
	echo '                      <li>Ralphy provides Squeezelite binaries with the additional features enabled.</li>'
	echo '                      <li>For more information on Squeezelite - see <a href="https://code.google.com/p/squeezelite/">Squeezelite Google code</a>.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </form>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_main_update_ralphy
#----------------------------------------------------------------------------------------

#------------------------------------------Reboot----------------------------------------
pcp_main_reboot() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Reboot" action="javascript:pcp_confirm('\''Reboot '$NAME'?'\'','\''reboot.cgi'\'')" method="get">'
	echo '                  <input type="submit" value="Reboot" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Reboot piCorePlayer after enabling or disabling HDMI output&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will reboot piCorePlayer.</p>'
	echo '                  <p><b>Note: </b>This will do the following:</p>'
	echo '                  <ul>'
	echo '                    <li>Shutdown piCore gracefully.</li>'
	echo '                    <li>Boot piCorePlayer from scratch using the latest settings.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
pcp_main_reboot
#----------------------------------------------------------------------------------------

#------------------------------------------Update pCP------------------------------------
pcp_main_update_pcp() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="InSitu" action="insitu_update.cgi" method="get">'
	echo '                  <input type="submit" value="Update pCP" />'
	echo '                  <input type="hidden" name="ACTION" value="initial" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Update piCorePlayer without removing the SD card&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This can be used when the SD card slot is not accessible.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Internet access is required.</li>'
	echo '                    <li>The current version of piCorePlayer will be completely overwritten.</li>'
	echo '                    <li>Additional extensions (ie. Jivelite, Shairport) will need to be reloaded.</li>'
	echo '                    <li>When the update has completed:</li>'
	echo '                    <ol>'
	echo '                      <li>select [SqueezeLite Settings] and confirm your "Audio output" settings.</li>'
	echo '                      <li>click [Save] and [Reboot].</li>'
	echo '                    </ol>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_main_update_pcp
#----------------------------------------------------------------------------------------

#------------------------------------------Save to USB-----------------------------------
pcp_main_save_usb() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Saveconfig" action="save2usb.cgi" method="get">'
	echo '                  <input type="submit" value="Save to USB" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Save your current configuration to the USB flash drive&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will copy the current configuration file to the USB flash drive.</p>'
	echo '                  <p>This configuration file can be used:</p>'
	echo '                  <ul>'
	echo '                    <li>as a backup</li>'
	echo '                    <li>after an update</li>'
	echo '                    <li>in another piCorePlayer.</li>'
	echo '                  </ul>'
	echo '                  <p><b>Note: </b>USB flash drive must be plugged into USB port.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_main_save_usb
#----------------------------------------------------------------------------------------

#------------------------------------------Advanced mode fieldset------------------------
if [ $MODE -ge $MODE_ADVANCED ]; then
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Advanced mode operations</legend>'
	echo '          <table class="bggrey percent100">'
fi
#----------------------------------------------------------------------------------------

#------------------------------------------Stop------------------------------------------
pcp_main_stop() {
	pcp_start_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Stop" action="stop.cgi" method="get">'
	echo '                  <input type="submit" value="Stop" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Stop Squeezelite&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will kill the Squeezelite process.</p>'
	echo '                  <p>Click [Restart] to start Squeezelite again.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Squeezelite running indicator will turn red.</li>'
	echo '                    <li>Squeezelite in the footer will turn red.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_main_stop
#----------------------------------------------------------------------------------------

#------------------------------------------Backup----------------------------------------
pcp_main_backup() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="backup" action="javascript:pcp_confirm('\''Do a backup on '$NAME'?'\'','\''backup.cgi'\'')" method="get">'
	echo '                  <input type="submit" value="Backup" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Backup your changes&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will do a piCore backup to your SD card.</p>'
	echo '                  <p>piCorePlayer does a backup after it changes any setting, so this option is really just for "peace of mind"'
	echo '                     before doing a shutdown or reboot.</p>'
	echo '                  <p><b>Note: </b>This will backup the following:</p>'
	echo '                  <ul>'
	echo '                    <li>Your configuration file.</li>'
	echo '                    <li>Your home directory.</li>'
	echo '                    <li>Files and directories defined in /opt/.filetool.lst</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_main_backup
#----------------------------------------------------------------------------------------

#------------------------------------------Shutdown--------------------------------------
pcp_main_shutdown() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Shutdown" action="javascript:pcp_confirm('\''Shutdown '$NAME'?'\'','\''shutdown.cgi'\'')" method="get">'
	echo '                  <input type="submit" value="Shutdown" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Shutdown piCorePlayer&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will shutdown piCorePlayer gracefully.</p>'
	echo '                  <p>To restart piCorePlayer you will need to remove then reapply the power.</p>'
	echo '                  <p><b>Note: </b>This option is not really required - piCorePlayer can be turned off at the switch.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_main_shutdown
#----------------------------------------------------------------------------------------

#------------------------------------------Beta mode fieldset----------------------------
if [ $MODE -ge $MODE_BETA ]; then
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Beta mode operations</legend>'
	echo '          <table class="bggrey percent100">'
fi
#----------------------------------------------------------------------------------------

#------------------------------------------Static IP-------------------------------------
pcp_main_static_ip(){
	pcp_start_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Static IP" action="xtras_staticip.cgi" method="get">'
	echo '                  <input type="submit" value="Static IP" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Static IP for wired networks&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This option allows you to set a static IP for wired networks (eth0).</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_static_ip
#----------------------------------------------------------------------------------------

#------------------------------------------Reset ALL-------------------------------------
pcp_main_reset_all() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Reset ALL" action="javascript:pcp_confirm('\''WARNING:\nYou are about to RESET your configuration file.'\'','\''writetoconfig.cgi?SUBMIT=Reset'\'')" method="get">'
	echo '                  <input type="submit" name="SUBMIT" value="Reset ALL" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Reset all settings in configuration file&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This command will reset all settings in the configuration file to the defaults that'
	echo '                     are defined in pcp-functions. </p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_reset_all
#----------------------------------------------------------------------------------------

#------------------------------------------Restore ALL-----------------------------------
pcp_main_restore_all() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Restore ALL" action="writetoconfig.cgi" method="get">'
	echo '                  <input type="submit" name="SUBMIT" value="Restore ALL" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Restore all settings in configuration file&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This command will restore all settings in the configuration file to those found in'
	echo '                     newconfig.cfg on USB flash memory.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_restore_all
#----------------------------------------------------------------------------------------

#------------------------------------------Resize FS-------------------------------------
pcp_main_resize_fs() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Resize FS" action="xtras_resize.cgi" method="get">'
	echo '                  <input type="submit" value="Resize FS" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Resize file system&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This command will resize the file system to fit the SD card.</p>'
	echo '                  <p>Only required if you need to add extra extensions.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_resize_fs
#----------------------------------------------------------------------------------------

#------------------------------------------Extensions------------------------------------
pcp_main_extensions() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Stop" action="xtras_extensions.cgi" method="get">'
	echo '                  <input type="submit" value="Extensions" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Search, load or delete piCore extensions&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This page gives you the option to search, load or delete piCore extensions.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_extensions
#----------------------------------------------------------------------------------------

#------------------------------------------Dosfsck---------------------------------------
pcp_main_dosfsck() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="DOS fsck" action="xtras_dosfsck.cgi" method="get">'
	echo '                  <input type="submit" value="DOS fsck" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>DOS file system check&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This option allows you to run dosfsck on the SD card.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_dosfsck
#----------------------------------------------------------------------------------------

#------------------------------------------Diagnostics-----------------------------------
pcp_main_diagnostics() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Diagnostics" action="diagnostics.cgi" method="get">'
	echo '                  <input type="submit" value="Diagnostics" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Go to Diagnostics page&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will go to the Diagnostics page.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_diagnostics
#----------------------------------------------------------------------------------------

#------------------------------------------Extras----------------------------------------
pcp_main_extras() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Extras" action="xtras.cgi" method="get">'
	echo '                  <input type="submit" value="Extras" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Go to Extras page&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will go to the Extras page.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_extras
#----------------------------------------------------------------------------------------

#------------------------------------------copy2fs----------------------------------------
pcp_main_copy2fs() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="copy2fs" action="xtras_copy2fs.cgi" method="get">'
	echo '                  <input type="submit" value="copy2fs" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Set copy2fs flag&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This sets the copy2fs flag so extensions are loaded into ram.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_copy2fs
#----------------------------------------------------------------------------------------

#------------------------------------------Developer mode fieldset-----------------------
if [ $MODE -ge $MODE_DEVELOPER ]; then
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Developer mode operations</legend>'
	echo '          <table class="bggrey percent100">'
fi
#----------------------------------------------------------------------------------------

#------------------------------------------Debug-----------------------------------------
pcp_main_debug() {
	pcp_start_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Debug" action="debug.cgi" method="get">'
	echo '                  <input type="submit" value="Debug" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Go to Debug page&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will go to the Debug page.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_debug
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'
