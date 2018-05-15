#!/bin/sh

# Version: 4.0.0 2018-05-15

. pcp-functions
. pcp-rpi-functions
. pcp-lms-functions
. pcp-wifi-functions

unset REBOOT_REQUIRED
unset MODIFY_OK
unset ERROR_FLG

pcp_html_head "Wifi WPA Settings" "GE"

pcp_picoreplayers_toolbar
pcp_controls
pcp_banner
pcp_navigation
pcp_httpd_query_string

[ x"" = x"$ACTION" ] && ACTION=Initial
WPACONFIGFILE=$WPASUPPLICANTCONF

#========================================================================================
# HTML end.
#----------------------------------------------------------------------------------------
pcp_html_end() {
	pcp_footer
	[ $MODE -ge $MODE_NORMAL ] && pcp_mode
	pcp_copyright
	echo '</body>'
	echo '</html>'
	exit
}

#========================================================================================
# WARNING messages
#----------------------------------------------------------------------------------------
[ $(pcp_kernel) = "pcpAudioCore" ] && ERRMSG1="Wifi may not work on the pcpAudioCore kernel." && ERROR_FLG=TRUE

if [ $(pcp_exists_wpa_supplicant) -eq 0 ]; then
	[ $(pcp_wifi_maintained_by_user) -eq 0 ] && ERRMSG3="Configuration maintained by user not piCorePlayer." && ERROR_FLG=TRUE
	[ $(pcp_wifi_update_config) -ne 0 ] && ERRMSG4="Configuration can not be maintained by piCorePlayer or wpa_cli." && ERROR_FLG=TRUE
else
	ERRMSG2="$WPASUPPLICANTCONF not found."
	ERROR_FLG=TRUE
fi

if [ "$WIFI" = "on" ]; then
	if [ $(pcp_exists_wpa_supplicant) -eq 0 ]; then
		if [ $(pcp_wifi_update_config) -eq 0 ] && [ $(pcp_wifi_maintained_by_pcp) -eq 0 ]; then
			MODIFY_OK=TRUE
		fi
	else
		MODIFY_OK=TRUE
	fi
	[ $MODIFY_OK ] || (ERRMSG5="Configuration can not be maintained by piCorePlayer."; ERROR_FLG=TRUE)
fi

pcp_wifi_error_messages() {
	if [ "$WIFI" = "on" ] && [ $ERROR_FLG ]; then
		echo '<table class="bggrey">'
		echo '  <tr class="warning">'
		echo '    <td>'
		echo '      <div style="color:white">'
		echo '        <p><b>WARNINGS:</b>'
		echo '          <ul>'
		for i in 1 2 3 4 5; do
			[ x"" != x"$(eval echo \$ERRMSG${i})" ] && echo '            <li>'$(eval echo \$ERRMSG${i})'</li>'
		done
		echo '          </ul>'
		echo '        </p>'
		echo '      </td>'
		echo '    </div>'
		echo '  </tr>'
		echo '</table>'
	fi
}

#========================================================================================
# Main.
#----------------------------------------------------------------------------------------
case "$ACTION" in
	Initial)
		pcp_wifi_error_messages
		if [ "$WIFI" = "on" ]; then
			pcp_table_textarea_top "Initial option" "" "30"
			pcp_wifi_read_wpa_supplicant "text"
			pcp_table_textarea_end
		fi
	;;
	Config)
		pcp_wifi_error_messages
		pcp_table_textarea_top "Config option" "" "50"
		pcp_wifi_update_filetool
		pcp_save_to_config
		pcp_wifi_read_wpa_supplicant "text"
		pcp_backup "nohtml"
		pcp_table_textarea_end
	;;
	Save)
		pcp_table_textarea_top "Save option" "" "100"
		pcp_wifi_update_filetool
		if [ "$WIFI" = "on" ]; then
			pcp_wifi_load_wifi_extns "text"
			pcp_wifi_load_wifi_firmware_extns "text"
			pcp_wifi_generate_passphrase "text"
			pcp_wifi_write_wpa_supplicant "text"
			pcp_backup "nohtml"
			pcp_wifi_read_wpa_supplicant "text"
		fi
		pcp_save_to_config
		pcp_backup "nohtml"
		pcp_table_textarea_end
	;;
#----------------------------------Developer options-------------------------------------
	Read)
		pcp_wifi_error_messages
		pcp_table_textarea_top "Read option" "" "30"
		pcp_wifi_read_wpa_supplicant "text"
		pcp_table_textarea_end
	;;
	Delete)
		pcp_table_textarea_top "Delete option" "" "30"
		rm -f $WPASUPPLICANTCONF
		[ $? -eq 0 ] && pcp_message OK "$WPASUPPLICANTCONF deleted." "text"
		unset WPA_SSID WPA_PASSWORD WPA_PW WPA_PSK WPA_PASSPHRASE WPA_KEY_MGMT WPA_ENCRYPTION WPA_HIDDENSSID
		pcp_table_textarea_end
	;;
	Remove)
		pcp_table_textarea_top "Remove option" "" "30"
		pcp_wifi_unload_wifi_extns "text"
		pcp_wifi_unload_wifi_firmware_extns "text"
		pcp_table_textarea_end
	;;
	Start)
		pcp_table_textarea_top "Start option" "" "30"
		/usr/local/etc/init.d/wifi wlan0 start
		pcp_table_textarea_end
	;;
	Stop)
		pcp_table_textarea_top "Stop option" "" "30"
		/usr/local/etc/init.d/wifi wlan0 stop
		pcp_table_textarea_end
	;;
	Status)
		pcp_table_textarea_top "Status option" "" "30"
		/usr/local/etc/init.d/wifi wlan0 status
		pcp_table_textarea_end
	;;
	Convert1)
		pcp_table_textarea_top "Convert option" "" "100"
		WPACONFIGFILE="/tmp/newconfig.cfg"
		if [ -f $WPACONFIGFILE ]; then
			pcp_wifi_read_newconfig "text"
			pcp_wifi_write_wpa_supplicant "text"
		fi
		pcp_table_textarea_end
	;;
	Convert2)
		pcp_table_textarea_top "Convert option" "" "100"
		WPACONFIGFILE="/tmp/wpa_supplicant.conf"
		if [ -f $WPACONFIGFILE ]; then
			pcp_wifi_read_wpa_supplicant "text"
			pcp_wifi_write_wpa_supplicant "text"
		fi
		pcp_table_textarea_end
	;;
	*)
		[ $DEBUG -eq 1 ] && echo "Case: Invalid"
		if [ "$WIFI" = "on" ]; then
			pcp_wifi_read_wpa_supplicant
		fi
	;;
esac

#========================================================================================
# Debug information.
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	pcp_table_top "Debug Information"
	pcp_debug_variables "html" ACTION WIFI WPA_SSID WPA_PSK WPA_PW WPA_PASSWORD WPA_PASSPHRASE WPA_ENCRYPTION WPA_HIDDENSSID RPI3INTWIFI RPIBLUETOOTH
	pcp_table_end
fi

#========================================================================================
# Main.
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form id="setwifi" name="setwifi" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Set wifi configuration</legend>'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
case "$WIFI" in
	on)
		WIFIon="checked"
		COLUMN1="column150"
		COLUMN2="column380"
	;;
	off)
		WIFIoff="checked"
		COLUMN1="column150"
		COLUMN2="column150"
	;;
esac
#--------------------------------------Wifi on/off---------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">'
echo '                  <p>Wifi</p>'
echo '                </td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <input class="small1" type="radio" name="WIFI" value="on" '$WIFIon'>On&nbsp;&nbsp;&nbsp;'
echo '                  <input class="small1" type="radio" name="WIFI" value="off" '$WIFIoff'>Off'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set wifi on or off&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Selecting wifi on will enable the remaining fields.</li>'
echo '                      <li>A reboot is required when wifi is turned on.</li>'
echo '                      <li>Turn wifi on if you have compatible USB wifi adaptor installed.</li>'
echo '                      <li>Setting wifi to off will improve boot times.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
if [ "$WIFI" = "on" ]; then
#--------------------------------------SSID----------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p>SSID</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="WPA_SSID"'
	echo '                         value="'$WPA_SSID'"'
	echo '                         maxlength="32"'
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter your wifi network SSID&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>Service Set Identifier (SSID).</li>'
	echo '                      <li>Use valid alphanumeric characters only.</li>'
	echo '                      <li>Maximum length of 32 characters.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#--------------------------------------Password------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p>PSK Password</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="large30"'
	echo '                         type="text"'
	echo '                         name="WPA_PASSWORD"'
	echo '                         value="'$WPA_PASSWORD'"'
	echo '                         maxlength="64"'
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter your wifi network password&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>Use valid alphanumeric characters only.</li>'
	echo '                      <li>Maximum length of 64 characters.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#--------------------------------------Passphrase----------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p>PSK Passphrase</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="large30"'
	echo '                         type="text"'
	echo '                         name="WPA_PASSPHRASE"'
	echo '                         value="'$WPA_PASSPHRASE'"'
	echo '                         maxlength="64"'
	echo '                         readonly'
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter your wifi network passphrase&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>Use valid alphanumeric characters only.</li>'
	echo '                      <li>Maximum length of 64 characters.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#--------------------------------------Security Mode-------------------------------------
	case "$WPA_ENCRYPTION" in
		WPA-PSK) WPA_ENCRYPTIONwpa="checked" ;;
		WEP) WPA_ENCRYPTIONwep="checked" ;;
		OPEN) WPA_ENCRYPTIONopen="checked" ;;
		*) WPA_ENCRYPTIONwpa="checked" ;;
	esac
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p>Security Mode</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="small1" type="radio" name="WPA_ENCRYPTION" value="WPA-PSK" '$WPA_ENCRYPTIONwpa'>WPA-PSK&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="WPA_ENCRYPTION" value="WEP" '$WPA_ENCRYPTIONwep'>WEP'
	echo '                  <input class="small1" type="radio" name="WPA_ENCRYPTION" value="OPEN" '$WPA_ENCRYPTIONopen'>OPEN'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set to your wifi network security level&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;WPA-PSK|WEP|Open&gt;</p>'
	echo '                    <p>Recommended: WPA-PSK</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#--------------------------------------Hidden SSID---------------------------------------
	case "$WPA_HIDDENSSID" in
		0) WPA_HIDDENSSIDno="checked" ;;
		1) WPA_HIDDENSSIDyes="checked" ;;
		*) WPA_HIDDENSSIDno="checked" ;;
	esac
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p>Hidden SSID</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="small1" type="radio" name="WPA_HIDDENSSID" value="1" '$WPA_HIDDENSSIDyes'>Yes&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="WPA_HIDDENSSID" value="0" '$WPA_HIDDENSSIDno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set hiddden SSID&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Select yes to use a hidden SSID.</p>'
	echo '                    <p><b>Note: </b>We do not recommend the use of a hidden SSID. '
	echo '                    This option is only for the convenience of users that have already setup a hidden SSID.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
fi
#--------------------------------------Built-in Wifi-------------------------------------
if [ $(pcp_rpi_has_inbuilt_wifi) -eq 0 ] || [ $TEST -eq 1 ]; then
	case "$RPI3INTWIFI" in
		on) RPIWIFIyes="checked" ;;
		off) RPIWIFIno="checked" ;;
	esac
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p>RPi built-in Wifi</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="small1" type="radio" name="RPI3INTWIFI" value="on" '$RPIWIFIyes'>On&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="RPI3INTWIFI" value="off" '$RPIWIFIno'>Off'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Turn off Raspberry Pi built-in wifi&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will load an overlay that disables built-in wifi.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#--------------------------------------Built-in Bluetooth--------------------------------
	case "$RPIBLUETOOTH" in
		on) RPIBLUETOOTHyes="checked" ;;
		off) RPIBLUETOOTHno="checked" ;;
	esac
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p>RPi built-in Bluetooth</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="small1" type="radio" name="RPIBLUETOOTH" value="on" '$RPIBLUETOOTHyes'>On&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="RPIBLUETOOTH" value="off" '$RPIBLUETOOTHno'>Off'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Turn off Raspberry Pi built-in bluetooth&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will load an overlay that disables built-in bluetooth.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
fi
#--------------------------------------Buttons------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'

if [ $(pcp_rpi_is_model_3Bplus) -eq 0 ]; then
	echo '                  <input type="hidden" name="RPI3BPLUS" value="true">'
else
	echo '                  <input type="hidden" name="RPI3BPLUS" value="false">'
fi

if [ "$WIFI" = "on" ]; then
	echo '                  <input type="submit" name="ACTION" value="Save">'
	echo '                  <input type="button" name="DIAGNOSTICS" onClick="location.href='\'''diag_wifi.cgi''\''" value="Diagnostics">'
else
	echo '                  <button type="submit" name="ACTION" value="Config">Save</button>'
fi

echo '                </td>'
echo '              </tr>'

if [ $MODE -ge $MODE_DEVELOPER ]; then
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="ACTION" value="Read">'
	echo '                  <input type="submit" name="ACTION" value="Delete">'
	echo '                  <input type="submit" name="ACTION" value="Remove">'
	echo '                  <input type="submit" name="ACTION" value="Start">'
	echo '                  <input type="submit" name="ACTION" value="Stop">'
	echo '                  <input type="submit" name="ACTION" value="Status">'
	echo '                </td>'
	echo '              </tr>'
fi

#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

if [ $DEBUG -eq 1 ]; then
#----------------------------------------------------------------------------------------
	pcp_table_top "[ DEBUG ] $WPASUPPLICANTCONF tests"
	[ $(pcp_exists_wpa_supplicant) -eq 0 ] &&
	echo '<p>[ INFO ] '$WPASUPPLICANTCONF' exists</p>' || echo '<p>[ ERROR ] '$WPASUPPLICANTCONF' does not exists.</p>'
	[ $(pcp_wifi_maintained_by_pcp) -eq 0 ] &&
	echo '<p>[ INFO ] '$WPASUPPLICANTCONF' "Maintained by piCorePlayer"</p>' || echo '<p>[ ERROR ] '$WPASUPPLICANTCONF' not "Maintained by piCorePlayer".</p>'
	pcp_table_end
#----------------------------------------------------------------------------------------
	WPACONFIGFILE="/tmp/newconfig.cfg"
	pcp_table_top "[ DEBUG ] $WPACONFIGFILE"
	pcp_textarea_inform "none" "cat ${WPACONFIGFILE}" 80
	if [ -f $WPACONFIGFILE ]; then
		pcp_toggle_row_shade
		echo '    <tr class="'$ROWSHADE'">'
		echo '      <td colspan="3">'
		echo '        <form name="wpatest1" action="'$0'" method="get">'
		echo '          <input type="submit" name="ACTION" value="Convert1">'
		echo '        </form>'
		echo '      </td>'
		echo '    </tr>'
	else
		pcp_message ERROR "$WPACONFIGFILE not found." "html"
	fi
	pcp_table_end
#----------------------------------------------------------------------------------------
	WPACONFIGFILE="/tmp/wpa_supplicant.conf"
	pcp_table_top "[ DEBUG ] $WPACONFIGFILE"
	pcp_textarea_inform "none" "cat ${WPACONFIGFILE}" 80
	if [ -f $WPACONFIGFILE ]; then
		pcp_toggle_row_shade
		echo '    <tr class="'$ROWSHADE'">'
		echo '      <td colspan="3">'
		echo '        <form name="wpatest2" action="'$0'" method="get">'
		echo '          <input type="submit" name="ACTION" value="Convert2">'
		echo '        </form>'
		echo '      </td>'
		echo '    </tr>'
	else
		pcp_message ERROR "$WPACONFIGFILE not found." "html"
	fi
	pcp_table_end
#----------------------------------------------------------------------------------------
	pcp_table_top "[ DEBUG ] $WPASUPPLICANTCONF"
	pcp_textarea_inform "none" "cat ${WPASUPPLICANTCONF}" 150
	pcp_table_end
#----------------------------------------------------------------------------------------
	pcp_table_top "[ DEBUG ] Installed extensions"
	pcp_wifi_all_extensions_installed "html"
	pcp_table_end
#----------------------------------------------------------------------------------------
	pcp_table_top "[ DEBUG ] $FILETOOLLST"
	pcp_textarea_inform "none" "cat $FILETOOLLST" 150
	pcp_table_end
fi
#----------------------------------------------------------------------------------------

#--------------------------------------Display Wifi information--------------------------
if [ "$WIFI" = "on" ]; then
	[ x"" = x"$(pcp_wlan0_mac_address)" ] && WLANMAC=" is missing - reboot or connect required." || WLANMAC=$(pcp_wlan0_mac_address)
	[ x"" = x"$(pcp_wlan0_ip)" ] && WLANIP=" is missing - reboot or connect required." || WLANIP=$(pcp_wlan0_ip)
#-----------------------------------------Wifi information-------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Wifi information</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150">'
	echo '                <input form="setwifi" type="submit" name="SUBMIT" value="Scan">'
	echo '              </td>'
	echo '              <td class="column380">'
	echo '                <p>Wifi MAC: '$WLANMAC'</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Wifi IP: '$WLANIP'</p>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
#-------------------------------------Display available wifi networks--------------------
	if [ "$SUBMIT" = "Scan" ]; then
		echo '<table class="bggrey">'
		echo '  <tr>'
		echo '    <td>'
		echo '      <div class="row">'
		echo '        <fieldset>'
		echo '          <legend>Available wifi networks</legend>'
		echo '          <table class="bggrey percent100">'
		pcp_start_row_shade
		echo '            <tr class="'$ROWSHADE'">'
		echo '              <td>'
		                      pcp_textarea_inform "none" "pcp_wifi_available_networks" 110
		echo '              </td>'
		echo '            </tr>'
		echo '          </table>'
		echo '        </fieldset>'
		echo '      </div>'
		echo '    </td>'
		echo '  </tr>'
		echo '</table>'
	fi
#----------------------------------------------------------------------------------------
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# AP Mode Page Link
#----------------------------------------------------------------------------------------
wifi_apmode_page() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>AP mode configuration page</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150">'
	echo '                <form action="wifi_apmode.cgi" method="get">'
	echo '                  <input type="submit" name="APmode" value="pCP AP Mode">'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Setup your piCorePlayer as a wifi AP&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>Disable wifi client above to enable this button.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_BETA ] && wifi_apmode_page
#----------------------------------------------------------------------------------------

pcp_html_end