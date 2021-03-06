#!/bin/sh

# Version: 5.0.0 2019-05-26

. pcp-functions

pcp_html_head "Write to Samba" "PH"

pcp_banner
pcp_running_script
pcp_remove_query_string
pcp_httpd_query_string

#========================================================================================
# Process Command section
#----------------------------------------------------------------------------------------
[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] COMMAND is: '$COMMAND'</p>'

pcp_table_top "SAMBA configuration"

case "$COMMAND" in
	setconfig)
		# Write the Global Section of the config file
		echo "[global]" > $SAMBACONF
		echo "    netbios name = ${NETBIOS}" >> $SAMBACONF
		echo "    workgroup = ${WGROUP}" >> $SAMBACONF
		echo "    log file = /var/log/%m.log" >> $SAMBACONF
		echo "    max log size = 1000" >> $SAMBACONF
		echo "    local master = no" >> $SAMBACONF
		echo "    security = user" >> $SAMBACONF
		echo "    map to guest = bad user" >> $SAMBACONF
		echo "    dns proxy = no" >> $SAMBACONF
		echo "    load printers = no" >> $SAMBACONF

		# Write the Individual Shares
		I=1

		while [ $I -le $SC ]
		do
			TST=$(eval echo "\${SHARE${I}}")
			if [ x"$TST" != "x" ]; then
				eval echo "[\${SHARE${I}}]" >> $SAMBACONF
				echo -n "    " >> $SAMBACONF
				eval echo "path = \${SHAREPATH${I}}" >> $SAMBACONF
				echo -n "    " >> $SAMBACONF
				if [ $(eval echo "\${SHAREMASK${I}}") != "" ]; then
					eval echo "create mask = \${SHAREMASK${I}}" >> $SAMBACONF
				else
					echo "create mask = 0664" >> $SAMBACONF
				fi
				echo "    browseable = yes" >> $SAMBACONF
				RO=$(eval echo "\${SHARERO${I}}")
				if [ "$RO" = "yes" ]; then
					echo "    read only = yes" >> $SAMBACONF
				else
					echo "    writeable = yes" >> $SAMBACONF
				fi
			fi
			I=$((I+1))
		done
		pcp_textarea_inform "$SAMBACONF" 'cat $SAMBACONF' 250

		pcp_backup
		grep -q "path" $SAMBACONF
		if [ $? -eq 0 ]; then
			echo -n '<p class="info">[ INFO ] '
			/usr/local/etc/init.d/samba4 restart
			echo '</p>'
		else
			echo '<p class="error">[ ERROR ] No Shares are set, Samba will be stopped</p>'
			/usr/local/etc/init.d/samba4 stop
		fi
	;;
	autostart)
		echo '<p class="info">[ INFO ] Setting SAMBA Autostart Status</p>'
		pcp_save_to_config
		pcp_backup
	;;
	setpw)
		echo '<p class="info">[ INFO ] Setting Share Password</p>'
		echo '<p class="info">[ INFO ] Removing old password</p>'
		smbpasswd -x tc >/dev/null 2>&1
		echo '<p class="info">[ INFO ] Adding new password for user: tc</p>'
		(echo "$SAMBAPASS"; echo "$SAMBAPASS") | smbpasswd -s -a tc
		pcp_backup
	;;
	*)
		echo '<p class="error">[ERROR] Web Page Error, Incorrect Command Submitted</p>'
	;;
esac

[ $DEBUG -eq 1 ] && pcp_textarea "Current $PCPCFG" "cat $PCPCFG" 150

pcp_table_middle
pcp_redirect_button "Go to LMS" "lms.cgi" 15
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'