#!/bin/sh

# Version: 0.01 2015-01-21 GE
#	Original - combined writeautostartlms.cgi and writeautostartfav.cgi
#	Added pcp_user_commands.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to Autostart" "GE" "5" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#========================================================================================
# Set Auto start LMS variables in config.cfg routine
#----------------------------------------------------------------------------------------
pcp_set_austostart_lms() {
	if [ "$SUBMIT" == "Clear" ]; then
		AUTOSTARTLMS=""
		A_S_LMS="Disabled"
	fi

	if [ "$A_S_LMS" == "Enabled" ]; then
		A_S_FAV="Disabled"
	fi

	# Save the encoded parameter to the config file, with quotes
	sudo sed -i "s/\(AUTOSTARTLMS=\).*/\1\"$AUTOSTARTLMS\"/" $CONFIGCFG
	sudo sed -i "s/\(A_S_LMS=\).*/\1\"$A_S_LMS\"/" $CONFIGCFG
	sudo sed -i "s/\(A_S_FAV=\).*/\1\"$A_S_FAV\"/" $CONFIGCFG

	echo '<p class="info">[ INFO ] Autostart LMS is set to: '$AUTOSTARTLMS'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Autostart LMS is: '$A_S_LMS'</p>'

	pcp_backup

	if [ "$SUBMIT" == "Test" ]; then
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Submit: '$SUBMIT'</p>'
		pcp_auto_start_lms
	fi
}

#========================================================================================
# Set Auto start FAV variables in config.cfg routine
#----------------------------------------------------------------------------------------
pcp_set_austostart_fav() {
	if [ "$SUBMIT" == "Clear" ]; then
		AUTOSTARTFAV=""
		A_S_FAV="Disabled"
	fi

	if [ "$A_S_FAV" == "Enabled" ]; then
		A_S_LMS="Disabled"
	fi

	# Save the encoded parameter to the config file, with quotes
	sudo sed -i "s/\(AUTOSTARTFAV=\).*/\1\"$AUTOSTARTFAV\"/" $CONFIGCFG
	sudo sed -i "s/\(A_S_FAV=\).*/\1\"$A_S_FAV\"/" $CONFIGCFG
	sudo sed -i "s/\(A_S_LMS=\).*/\1\"$A_S_LMS\"/" $CONFIGCFG

	echo '<p class="info">[ INFO ] Auto start FAV is set to: '$AUTOSTARTFAV'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Auto start FAV is: '$A_S_FAV'</p>'

	pcp_backup

	if [ "$SUBMIT" == "Test" ]; then
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Submit: '$SUBMIT'</p>'
		pcp_auto_start_fav
	fi
}

#========================================================================================
# Set USER_COMMAND_x variables in config.cfg routine
#----------------------------------------------------------------------------------------
pcp_set_user_commands() {
	# Save the encoded parameter to the config file, with quotes
	sudo sed -i "s/\(USER_COMMAND_1=\).*/\1\"$USER_COMMAND_1\"/" $CONFIGCFG
	sudo sed -i "s/\(USER_COMMAND_2=\).*/\1\"$USER_COMMAND_2\"/" $CONFIGCFG
	sudo sed -i "s/\(USER_COMMAND_3=\).*/\1\"$USER_COMMAND_3\"/" $CONFIGCFG

	echo '<p class="info">[ INFO ] User command #1 is set to: '$USER_COMMAND_1'<br />'
	echo '                [ INFO ] User command #2 is set to: '$USER_COMMAND_2'<br />'
	echo '                [ INFO ] User command #3 is set to: '$USER_COMMAND_3'</p>'

	pcp_backup
}

#========================================================================================
# Main routine
#----------------------------------------------------------------------------------------
case "$AUTOSTART" in
	LMS)
		pcp_set_austostart_lms
		;;
	FAV)
		pcp_set_austostart_fav
		;;
	CMD)
		pcp_set_user_commands
		;;
esac

#----------------------------------------------------------------------------------------

[ $DEBUG = 1 ] && pcp_show_config_cfg
pcp_go_back_button

echo '</body>'
echo '</html>'