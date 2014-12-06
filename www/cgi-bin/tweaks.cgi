#!/bin/sh

# Version: 0.05 2014-10-02 GE
#	Activated $MODE=5 for AUTOSTARTLMS.

# Version: 0.04 2014-09-10 GE
#   Added reformatted html.

# Version: 0.03 2014-09-09 GE
#   Added Auto start LMS command.

# Version: 0.02 2014-09-06 SBP
#   Added cronjob.

# Version: 0.01 2014-08-06 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <title>pCP - Tweaks</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Tweaks" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_controls
pcp_banner
pcp_navigation

# Change password - STILL UNDER DEVELOPMENT
# Note: changing passwords through a script over html is not very secure

echo '<table class="sframe" cellspacing="0" cellpadding="0" width="960">'
echo '  <tr>'
echo '    <td class="sframe">'
echo '      <table class="cfgframe" cellspacing="2" cellpadding="0" width="100%" align="center">'
echo '        <form name="password" action="changepassword.cgi" method="get">'
echo '          <tr>'
echo '            <td colspan="2" class="header"><nobr>GENERAL TWEAKS.</nobr></td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td class="title" width=20%>Password for "'$(pcp_tc_user)'"</td>'
echo '            <td class="content" width=80%>'
echo '              <input type="password" id="NEWPASSWORD" name="NEWPASSWORD" size="32" maxlength="26">'
echo '                Enter new password</td>'
echo '          <tr>'
echo '            <td class="title" width=20%>&nbsp;</td>'
echo '            <td class="content" width=80%>'
echo '              <input type="password" id="NEWPASSWORD" name="NEWPASSWORD" size="32" maxlength="26">'
echo '                Confirm new password</td>'
echo '          <tr>'
echo '            <td colspan=2 class="btnline" >'
echo '              <input type="submit" name="submit" value="Submit">&nbsp;'
echo '            </td>'
echo '          </tr>'
echo '        </form>'
echo '      </table>'
echo '      <br />'

[ -f /etc/sysconfig/timezone ] && . /etc/sysconfig/timezone

echo '      <table class="cfgframe" cellspacing="2" cellpadding="0" width="100%" align="center">'
echo '        <form name="tzone" action="timezone.cgi" method="get">'
echo '          <tr>'
echo '            <td class="title">Timezone</td>'
echo '            <td class="content" width=80%>'
echo '              <input type="text" id="TIMEZONE" name="TIMEZONE" size="32" maxlength="26" value="'$TZ'">'
echo '                Cut and paste your TIMEZONE from this <a href="http://wiki.openwrt.org/doc/uci/system#time.zones" target="_blank">list</a>.'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td colspan=2 class="btnline" >'
echo '              <input type="submit" name="submit" value="Submit">&nbsp;'
echo '            </td>'
echo '          </tr>'
echo '        </form>'
echo '      </table>'
echo '      <br />'

echo '      <table class="cfgframe" cellspacing="2" cellpadding="0" width="100%" align="center">'
echo '        <form name="squeeze" action="writetohost.cgi" method="get">'
echo '          <tr>'
echo '            <td class="title" width=20%>Host name</td>'
echo '            <td class="content" width=80%>'
echo '              <input type="text" id="HOST" name="HOST" size="32" maxlength="26" value="'$HOST'">'
echo '                Provide a host name, so the player is easier to identify on your LAN'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td colspan=2 class="btnline" >'
echo '              <input type="submit" name="submit" value="Submit">&nbsp;'
echo '            </td>'
echo '          </tr>'
echo '        </form>'
echo '      </table>'
echo '      <br />'

# Function in order to check the radiobutton according to what is present in config file
case "$OVERCLOCK" in 
	NONE)
		OCnone="selected"
		;;
	MILD)
		OCmild="selected"
		;;
	MODERATE)
		OCmoderate="selected"
		;;
	*)
		OCnone=""
		OCmild=""
		OCmoderate=""
		;;
esac

if [ $DEBUG = 1 ]; then 
	echo '<p class="debug">[ DEBUG ] $OVERCLOCK: '$OVERCLOCK'<br />'
	echo '                 [ DEBUG ] $OCnone: '$OCnone'<br />'
	echo '                 [ DEBUG ] $OCmild: '$OCmild'<br />'
	echo '                 [ DEBUG ] $OCmoderate: '$OCmoderate'</p>'
fi

echo '      <table class="cfgframe" cellspacing="2" cellpadding="0" width="100%" align="center">'
echo '        <form name="overclock" action= "writetooverclock.cgi" method="get">'
echo '          <tr class="odd">'
echo '            <td class="title" width=20%><p>Overclock</p></td>'
echo '            <td class="content" width=80%>'
echo '              <select name="OVERCLOCK">'
echo '                <option value="NONE" '$OCnone'> No overclocking </option>'
echo '                <option value="MILD" '$OCmild'> Mild overclocking </option>'
echo '                <option value="MODERATE" '$OCmoderate'> Moderate overclocking </option>'
echo '              </select>'
echo '                Change overclocking - If you fail to boot, then hold down the shift key during booting.'
echo '                Or you might have to edit the config.txt file manually.'
echo '                Reboot is needed.'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td colspan=2 class="btnline" >'
echo '              <input type="submit" name="submit" value="Submit">&nbsp;'
echo '            </td>'
echo '          </tr>'
echo '        </form>'
echo '      </table>'
echo '      <br />'

#******************************************************* 2014-09-09 GE *************************************************************
# Decode variables using httpd, no quotes
if [ $MODE -gt 4 ]; then
	AUTOSTARTLMS=`sudo /usr/local/sbin/httpd -d $AUTOSTARTLMS`

	echo '      <table class="cfgframe" cellspacing="2" cellpadding="0" width="100%" align="center">'
	echo '        <form name="autostartlms" action="autostartlms.cgi" method="get">'
	echo '          <tr>'
	echo '            <td class="title">Auto start LMS</td>'
	echo '            <td class="content" width=80%>'
	echo '              <input type="text" id="AUTOSTARTLMS" name="AUTOSTARTLMS" size="100" maxlength="254" value="'$AUTOSTARTLMS'">'
	echo '                Cut and paste your auto start LMS command.'
	echo '            </td>'
	echo '          </tr>'
	echo '          <tr>'
	echo '            <td colspan=2 class="btnline" >'
	echo '              <input type="submit" name="submit" value="Submit">&nbsp;'
	echo '            </td>'
	echo '          </tr>'
	echo '        </form>'
	echo '      </table>'
fi
#******************************************************* 2014-09-09 GE *************************************************************

echo '    </td>'
echo '  </tr>'
echo '</table>'

echo '<h2>[ INFO ] Current overclocking settings</h2>'

case $OVERCLOCK in
	NONE)
		echo '<p class="info">Overclocking is: '$OVERCLOCK'<br /><br />'
		echo '                arm_freq=700<br />'
		echo '                core_freq=250<br />'
		echo '                sdram_freq=400<br />'
		echo '                force_turbo=1</p>'
		;;
	MILD)
		echo '<p class="info">Overclocking is: '$OVERCLOCK'<br /><br />'
		echo '                arm_freq=800<br />' 
		echo '                core_freq=250<br />'
		echo '                sdram_freq=400<br />'
		echo '                force_turbo=1</p>'
		;;
	MODERATE)
		echo '<p class="info">Overclocking is: '$OVERCLOCK'<br /><br />'
		echo '                arm_freq=900<br />'
		echo '                core_freq=333<br />'
		echo '                sdram_freq=450<br />'
		echo '                force_turbo=0</p>'
		;;
esac

# Function in order to check the CMD-radiobutton according to what is present in config file
case "$CMD" in 
	Default)
		CMDdefault="checked"
		;;
	Slow)
		CMDslow="checked"
		;;
	*)
		CMDdefault=""
		CMDslow=""
		;;
esac

if [ $DEBUG = 1 ]; then 
	echo '<p class="debug">[ DEBUG ] $CMD: '$CMD'<br />'
	echo '                 [ DEBUG ] $CMDdefault: '$CMDdefault'<br />'
	echo '                 [ DEBUG ] $CMDslow: '$CMDslow'</p>'
fi

# Function in order to check the FIQ-split radiobutton according to what is present in config file

if [ $FIQ = 0x1 ]; then selected1="selected"; else selected1=""; fi
if [ $FIQ = 0x2 ]; then selected2="selected"; else selected2=""; fi
if [ $FIQ = 0x3 ]; then selected3="selected"; else selected3=""; fi
if [ $FIQ = 0x4 ]; then selected4="selected"; else selected4=""; fi
if [ $FIQ = 0x7 ]; then selected5="selected"; else selected5=""; fi
if [ $FIQ = 0x8 ]; then selected6="selected"; else selected6=""; fi

if [ $DEBUG = 1 ]; then 
	echo '<p class="debug">[ DEBUG ] $FIQ: '$FIQ'<br />'
	echo '                 [ DEBUG ] $selected1: '$selected1'<br />'
	echo '                 [ DEBUG ] $selected2: '$selected2'<br />'
	echo '                 [ DEBUG ] $selected3: '$selected3'<br />'
	echo '                 [ DEBUG ] $selected4: '$selected4'<br />'
	echo '                 [ DEBUG ] $selected5: '$selected5'<br />'
	echo '                 [ DEBUG ] $selected6: '$selected6'</p>'
fi

# Function in order to check the ALSA-radiobutton according to what is present in config file
case "$ALSAlevelout" in 
	Default)
		ALSAdefault="checked"
		;;
	Custom)
		ALSAcustom="checked"
		;;
	*)
		ALSAdefault=""
		ALSAcustom=""
		;;
esac

if [ $DEBUG = 1 ]; then 
	echo '<p class="debug">[ DEBUG ] $ALSAlevelout: '$ALSAlevelout'<br />'
	echo '                 [ DEBUG ] $ALSAdefault: '$ALSAdefault'<br />'
	echo '                 [ DEBUG ] $ALSAcustom: '$ALSAcustom'</p>'
fi

echo '<table class="sframe" cellspacing="0" cellpadding="0" width="960">'
echo '  <form name="setaudiotweaks" action="writetoaudiotweak.cgi" method="get">'
echo '    <tr>'
echo '      <td class="sframe">'
echo '        <table class="cfgframe" cellspacing="2" cellpadding="0" width="100%" align="center">'
echo '          <tr>'
echo '            <td colspan="2" class="header"><nobr>AUDIO TWEAKS.</nobr></td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td class="title" width=20%>OTG-Speed</td>'
echo '            <td class="content" width=80%>'
echo '              <input type="radio" name="CMD" id="not enabled" value="Default" '$CMDdefault'>Default'
echo '              <input type="radio" name="CMD" id="Custom" value="Slow" '$CMDslow'>dwc_otg.speed=1'
echo '                <br />'
echo '                Often needed for C-Media based DACs, try to use "dwc_otg.speed=1" if sound is crackling'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td class="title">ALSA output level</td>'
echo '            <td class="content">'
echo '              <input type="radio" name="ALSAlevelout" id="Default" value="Default" '$ALSAdefault'>Default'
echo '              <input type="radio" name="ALSAlevelout" id="Custom" value="Custom" '$ALSAcustom'>Custom ALSA output level'
echo '                <br />'
echo '                Use only if you have changed ALSA output level via ALSA-mixer, allows custom output level after reboot. <span style="color:blue;" title="Use alsamixer via SHH, and save your custom settings by sudo amixer store">HELP</span>'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td class="title">FIQ-Split acceleration</td>'
echo '            <td class="content">'
echo '              <select name="FIQ">'
echo '                <option value="0x1" '$selected1'> 1. Accelerate non-periodic split transactions - Value 0x1 </option>'
echo '                <option value="0x2" '$selected2'> 2. Accelerate periodic split transactions - Value 0x2 </option>'
echo '                <option value="0x3" '$selected3'> 3. Accelerate all except high-speed isochronous transactions - Value 0x3 </option><br />'
echo '                <option value="0x4" '$selected4'> 4. Accelerate high-speed isochronous transactions - Value 0x4 </option><br />'
echo '                <option value="0x7" '$selected5'> 5. Accelerate all transactions DEFAULT - Value 0x7 </option>'
echo '                <option value="0x8" '$selected6'> 6. Enable Interrupt/Control Split Transaction hack - Value 0x8 </option><br />'
echo '              </select>'
echo '              <br />'
echo '              Change FIQ_FSM USB settings. This might solve USB audio problems. Important for specific USB-DACs - like the Naim DAC-V1 card, try option 1, 2, 3 or 8. Reboot is needed.'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td colspan=2 class="btnline" >'
echo '              <input type="submit" name="submit" value="Submit">&nbsp;'
echo '            </td>'
echo '          </tr>'
echo '        </table>'
echo '      </td>'
echo '    </tr>'
echo '  </form>'
echo '</table>'

# Info section:

echo '<h2>[ INFO ] Current ALSA output level</h2>'
case $ALSAlevelout in
	Default)
		echo '<p class="info">Default - ALSA output level is used<br /></p>'
		;;
	Custom)
		echo '<p class="info">Custom - ALSA output level will be defined from your custom settings.<br /></p>'
		;;
esac

echo '<h2>[ INFO ] Current FIG-split acceleration settings</h2>'
case $FIQ in
	0x1)
		echo '<p class="info">FIQ-split value is: '$FIQ'<br />'
		echo '                Accelerate non-periodic split transactions</p>'
		;;
	0x2)
		echo '<p class="info">FIQ-split value is: '$FIQ'<br />'
		echo '                Accelerate periodic split transactions</p>'
		;;
	0x3)
		echo '<p class="info">FIQ-split value is: '$FIQ'<br />'
		echo '                Accelerate all except high-speed isochronous transactions</p>'
		;;
	0x4)
		echo '<p class="info">FIQ-split value is: '$FIQ'<br />'
		echo '                Accelerate high-speed isochronous transactions</p>'
		;;
	0x7)
		echo '<p class="info">FIQ-split value is: '$FIQ'<br />'
		echo '                Accelerate all transactions - DEFAULT</p>'
		;;
	0x8)
		echo '<p class="info">FIQ-split value is: '$FIQ'<br />'
		echo '                Enable Interrupt/Control Split Transaction hack</p>'
		;;
	*)
		echo '<p class="error">FIQ-split value is: INVALID</p>'
		;;
esac

#******************************************************* 2014-09-04 SBP *************************************************************
# Function in order to check the CRON Job schedule according to what is present in config file
pcp_variables

if [ $REBOOT = Enabled ]; then REBOOT_Y="checked"; else REBOOT_Y=""; fi
if [ $REBOOT = Disabled ]; then REBOOT_N="checked"; else REBOOT_N=""; fi
if [ $RESTART = Enabled ]; then RESTART_Y="checked"; else RESTART_Y=""; fi
if [ $RESTART = Disabled ]; then RESTART_N="checked"; else RESTART_N=""; fi

if [ $DEBUG = 1 ]; then 
	echo '<p class="debug">[ DEBUG ] $REBOOT: '$REBOOT'<br />'
	echo '                 [ DEBUG ] $REBOOT_Y: '$REBOOT_Y' <br />'
	echo '                 [ DEBUG ] $REBOOT_N: '$REBOOT_N' <br />'
	echo '                 [ DEBUG ] $RESTART: '$RESTART'<br  />'
	echo '                 [ DEBUG ] $RESTART_Y: '$RESTART_Y' <br />'
	echo '                 [ DEBUG ] $RESTART_N: '$RESTART_N' <br />'
	echo '                 [ DEBUG ] $RB_H: '$RB_H' <br />'
	echo '                 [ DEBUG ] $RB_WD: '$RB_WD' <br />'
	echo '                 [ DEBUG ] $RB_DMONTH: '$RB_DMONTH' <br />'
	echo '                 [ DEBUG ] $RS_H: '$RS_H' <br />'
	echo '                 [ DEBUG ] $RS_WD: '$RS_WD' <br />'
	echo '                 [ DEBUG ] $RS_DMONTH: '$RS_DMONTH' <br />'
fi

echo '<table class="sframe" cellspacing="0" cellpadding="0" width="960">'
echo '  <form name="cronjob" action="writetocronjob.cgi" method="get">'
echo '    <tr>'
echo '      <td class="sframe">'
echo '        <table class="cfgframe" cellspacing="2" cellpadding="0" width="100%" align="center">'
echo '          <tr>'
echo '            <td colspan="3" class="header"><nobr>SCHEDULE CRON JOBS.   (Please fill out the fields. If you use * it means every hour, every day etc)</nobr></td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td class="title" width=20%>Schedule reboot</td>'
echo '            <td class="content" width=50%>'
echo '              <label for="RB_H">Hour:</label>'
echo '              <input type="text" name="RB_H" id="RB_H" maxlength="2" size="2" value='$RB_H' />'
echo '              <label for="RB_WD">&nbsp;&nbsp;Weekday (0-7):</label>'
echo '              <input type="text" name="RB_WD" id="RB_WD" maxlength="1" size="1" value='$RB_WD' />'
echo '              <label for="RB_DMONTH">&nbsp;&nbsp;Day of Month:</label>'
echo '              <input type="text" name="RB_DMONTH" id="RB_DMONTH" maxlength="2" size="2" value='$RB_DMONTH' />'
echo '            </td>'
echo '            <td class="content" width=50%>'
echo '              <input type="radio" name="REBOOT" id="Scheduled" value="Enabled" '$REBOOT_Y'>Enabled'
echo '              <input type="radio" name="REBOOT" id="Scheduled" value="Disabled" '$REBOOT_N'>Disabled'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td class="title" width=20%>Schedule restart Squeezelite</td>'
echo '            <td class="content" width=40%>'
echo '              <label for="RS_H">Hour:</label>'
echo '              <input type="text" name="RS_H" id="RS_H" maxlength="2" size="2" value='$RS_H' />'
echo '              <label for="RS_WD">&nbsp;&nbsp;Weekday (0-7):</label>'
echo '              <input type="text" name="RS_WD" id="RS_WD" maxlength="1" size="1" value='$RS_WD' />'
echo '              <label for="RS_DMONTH">&nbsp;&nbsp;Day of Month:</label>'
echo '              <input type="text" name="RS_DMONTH" id="RS_DMONTH" maxlength="2" size="2" value='$RS_DMONTH' />'
echo '            </td>'
echo '            <td class="content" width=50%>'
echo '              <input type="radio" name="RESTART" id="Scheduled" value="Enabled" '$RESTART_Y'>Enabled'
echo '              <input type="radio" name="RESTART" id="Scheduled" value="Disabled" '$RESTART_N'>Disabled'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td colspan=3 class="btnline" >'
echo '              <input type="submit" name="submit" value="Submit">&nbsp;'
echo '            </td>'
echo '          </tr>'
echo '        </table>'
echo '      </td>'
echo '    </tr>'
echo '  </form>'
echo '</table>'
#******************************************************* 2014-09-04 SBP *************************************************************

[ $DEBUG = 1 ] && pcp_show_config_cfg
pcp_refresh_button
pcp_footer

echo '</body>'
echo '</html>'