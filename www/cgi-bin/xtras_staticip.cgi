#!/bin/sh

# Version: 0.01 2015-04-24 GE
#   Original version.

#========================================================================================
# This script sets a static IP. Initially only supports ethernet not wireless.
# The steps below follow the de-facto tiny core method of setting static IP address
# that is recommended in a few forum threads.
#
#   1. Set "nodhcp" bootcode
#   2. Create eth0.sh
#   3. Add /opt/eth0.sh to bootlocal.sh
#
# Complications:
#   1. wireless?  wifi.sh
#   2. eth0, what about eth1 or wlan0
#   3. /proc/cmdline only updated from /mnt/mmcblk0p1/cmdline.txt at boot time
#   4. /etc/init.d/settime.sh doesn't run with nodhcp bootcode.
#----------------------------------------------------------------------------------------

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras - Static IP" "GE"

#DEBUG=1
#MODE=99

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script

STATICIP=/opt/eth0.sh

#========================================================================================
# Add/remove $STATICIP to line 3 of /opt/bootlocal.sh script
#
# -rwxrwxr-x    1 tc       staff          197 Apr 24 10:18 bootlocal.sh
# -rwxr-xr-x    1 root     staff          284 Apr 19 22:39 bootsync.sh
#----------------------------------------------------------------------------------------
pcp_edit_localboot() {
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Writing /opt/bootlocal.sh...</p>'
	grep -v eth0.sh /opt/bootlocal.sh >/opt/bootlocal.sh~
	sudo chmod 755 /opt/bootlocal.sh~
	sudo mv /opt/bootlocal.sh~ /opt/bootlocal.sh
	[ $1 = "add" ] && sed -i "4i /opt/eth0.sh" /opt/bootlocal.sh
}

#========================================================================================
# Delete/add nodhcp boot code to /mnt/mmcblk0p1/cmdline.txt
#----------------------------------------------------------------------------------------
pcp_nodhcp_bootcode() {
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Writing /mnt/mmcblk0p1/cmdline.txt...</p>'
	pcp_mount_mmcblk0p1_nohtml >/dev/null
	if mount | grep $VOLUME >/dev/null; then
		sed -i 's/nodhcp //g' /mnt/mmcblk0p1/cmdline.txt
		[ $1 = "add" ] && sed -i 's/^/nodhcp /' /mnt/mmcblk0p1/cmdline.txt
		pcp_umount_mmcblk0p1_nohtml >/dev/null
	else
		[ $DEBUG = 1 ] && echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
	fi
}

#========================================================================================
# Read eth0 script
#----------------------------------------------------------------------------------------
pcp_read_script() {
	set -- `cat $STATICIP | grep ifconfig`
	IP=$3
	NETMASK=$5
	BROADCAST=$7
	set -- `cat $STATICIP | grep route`
	GATEWAY=$5
}

#========================================================================================
# Write eth0 script
#
#  1. Look into search gateway
#----------------------------------------------------------------------------------------
pcp_write_script() {
	echo '#!/bin/sh' >$STATICIP
	echo '# Generated by piCorePlayer' >>$STATICIP
	echo 'echo "[ INFO ] Running $0..."' >>$STATICIP
	echo 'ifconfig eth0 '$IP' netmask '$NETMASK' broadcast '$BROADCAST' up' >>$STATICIP
	echo 'route add default gw '$GATEWAY >>$STATICIP
#	echo 'echo search '$GATEWAY' > /etc/resolv.conf' >>$STATICIP
	echo 'echo nameserver '$GATEWAY' > /etc/resolv.conf' >>$STATICIP
	echo '/etc/init.d/settime.sh' >>$STATICIP
	chmod ugo+x $STATICIP
}

#========================================================================================
# Read eth0 script
#----------------------------------------------------------------------------------------
pcp_read_script() {
	set -- `cat $STATICIP | grep ifconfig`
	IP=$3
	NETMASK=$5
	BROADCAST=$7
	set -- `cat $STATICIP | grep route`
	GATEWAY=$5
}

#========================================================================================
# Display debug information
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	if [ $DEBUG = 1 ]; then 
		echo '<p class="debug">[ DEBUG ] $IP: '$IP'<br />'
		echo '                 [ DEBUG ] $NETMASK: '$NETMASK'<br />'
		echo '                 [ DEBUG ] $BROADCAST: '$BROADCAST'<br />'
		echo '                 [ DEBUG ] $GATEWAY: '$GATEWAY'</p>'
	fi
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'

pcp_httpd_query_string

case "$SUBMIT" in
	Save)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Writing '$STATICIP'...</p>'
		pcp_write_script
		if [ $DHCP = "off" ]; then
			pcp_nodhcp_bootcode add
			pcp_edit_localboot add
		else
			pcp_nodhcp_bootcode delete
			pcp_edit_localboot delete
		fi
		pcp_backup >/dev/null
		;;
	*)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Reading '$STATICIP'...</p>'
		;;
esac

pcp_debug_info
pcp_read_script

#========================================================================================
# Look for nodhcp boot code in /mnt/mmcblk0p1/cmdline.txt
#----------------------------------------------------------------------------------------
pcp_mount_mmcblk0p1_nohtml >/dev/null
if mount | grep $VOLUME >/dev/null; then
	cat /mnt/mmcblk0p1/cmdline.txt | grep nodhcp >/dev/null
	case "$?" in 
		0)
			[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] NODHCP boot code found in /mnt/mmcblk0p1/cmdline.txt.</p>'
			NODHCPYES="checked"
			DHCP="off"
			;;
		*)
			[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] NODHCP boot code not found in /mnt/mmcblk0p1/cmdline.txt.</p>'
			NODHCPNO="checked"
			DHCP="on"
			;;
	esac
	pcp_umount_mmcblk0p1_nohtml >/dev/null
else
	[ $DEBUG = 1 ] && echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
fi

echo '    </td>'
echo '  </tr>'
echo '</table>'
#========================================================================================
# Start table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="staticip" action="xtras_staticip.cgi" method="get" id="staticip">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Set static IP</legend>'
echo '            <table class="bggrey percent100">'
echo '              <tr class="warning">'
echo '                <td colspan="3">'
echo '                  <p style="color:white"><b>Note:</b> ONLY for wired network - eth0, will NOT work with wifi - wlan0.</b></p>'
echo '                </td>'
echo '              </tr>'
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">DHCP</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="small1" type="radio" id="DHCP" name="DHCP" value="on" '$NODHCPNO'>On&nbsp;&nbsp;'
echo '                  <input class="small1" type="radio" id="DHCP" name="DHCP" value="off" '$NODHCPYES'>Off'
echo '                </td>'
echo '                <td>'
echo '                  <p>Turn DCHP on or off (static IP)&nbsp;&nbsp;'
echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>To set a static IP you need to turn DHCP off.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">Static IP address</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="large15" type="text" id="IP" name="IP" value="'$IP'">'
echo '                </td>'
echo '                <td>'
echo '                  <p class="row">Set static IP address&nbsp;&nbsp;'
echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Your static IP must be unique and not clash with any other IP on your network.</li>'
echo '                      <li>Your static IP must not be in the range of IP addresses controlled by DHCP.</li>'
echo '                    </ul>'
echo '                    <p><b>Example: </b>192.168.1.123</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">Netmask</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="large15" type="text" id="NETMASK" name="NETMASK" value="'$NETMASK'">'
echo '                </td>'
echo '                <td>'
echo '                  <p class="row">Set netmask address&nbsp;&nbsp;'
echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>The netmask must be the same on all your devices.</p>'
echo '                    <p><b>Example: </b>255.255.255.0</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">Broadcast</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="large15" type="text" id="BROADCAST" name="BROADCAST" value="'$BROADCAST'">'
echo '                </td>'
echo '                <td>'
echo '                  <p class="row">Set broadcast address&nbsp;&nbsp;'
echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>The broadcast address is fixed and can not be used for other purposes.</p>'
echo '                    <p><b>Example: </b>192.168.1.255</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">Default gateway</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="large15" type="text" id="GATEWAY" name="GATEWAY" value="'$GATEWAY'">'
echo '                </td>'
echo '                <td>'
echo '                  <p class="row">Set default gateway address&nbsp;&nbsp;'
echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>The gateway address is usually your modem IP address.</p>'
echo '                    <p><b>Example: </b>192.168.1.1 or 192.168.1.254</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
pcp_incr_id
pcp_toggle_row_shade
echo '              </tr>'
echo '              <tr>'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
[ $MODE = 99 ] &&
echo '                  <input type="submit" name="SUBMIT" value="Read">'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

if [ $MODE = 99 ]; then
	#========================================================================================
	# Display current $STATICIP
	#----------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="static_ip" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Current '$STATICIP'</legend>'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "cat $STATICIP" 100
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'

	#========================================================================================
	# Display current /etc/resolv.conf
	#----------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="resolv.conf" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Current /etc/resolv.conf</legend>'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "cat /etc/resolv.conf" 25
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	#----------------------------------------------------------------------------------------

	#========================================================================================
	# Display current /mnt/mmcblk0p1/cmdline.txt
	#----------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="cmdline.txt" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Current /mnt/mmcblk0p1/cmdline.txt</legend>'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_mount_mmcblk0p1_nohtml >/dev/null
	                        pcp_textarea_inform "none" "cat /mnt/mmcblk0p1/cmdline.txt" 25
	                        pcp_umount_mmcblk0p1_nohtml >/dev/null
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	#----------------------------------------------------------------------------------------

	#========================================================================================
	# Display current /opt/bootlocal.sh
	#----------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="bootlocal.sh" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Current /opt/bootlocal.sh</legend>'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "cat /opt/bootlocal.sh" 70
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	#----------------------------------------------------------------------------------------
fi

pcp_footer

echo '</body>'
echo '</html>'