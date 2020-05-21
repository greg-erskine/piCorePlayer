#!/bin/sh

# Version: 7.0.0 2020-05-22

. pcp-functions

pcp_html_head "xtras ALSA equal" "GE"

pcp_controls
pcp_navbar
pcp_httpd_query_string
pcp_remove_query_string

ASOUNDCONF=/etc/asound.conf

#========================================================================================
# Find list of current equalizer controls in asound, and set device
#----------------------------------------------------------------------------------------

EQUALDEVICES=$(cat $ASOUNDCONF | grep pcm.equal | cut -d'{' -f1 | awk -F'pcm.' '{print $2}')

for j in $EQUALDEVICES; do
	[ "$j" = "$CUR_EQUAL_DEVICE" ] && break
done

[ "$CUR_EQUAL_DEVICE" = "" ] && CUR_EQUAL_DEVICE="equal"

SET_EQUAL="sudo amixer -D $CUR_EQUAL_DEVICE cset numid="
BAND=1
PRESETS=0
i=1

#========================================================================================
# Labels for equalizer bands
#----------------------------------------------------------------------------------------
LB1="31 Hz"
LB2="63 Hz"
LB3="125 Hz"
LB4="250 Hz"
LB5="500 Hz"
LB6="1 kHz"
LB7="2 kHz"
LB8="4 kHz"
LB9="8 kHz"
LB10="16 kHz"

pcp_equal_devices_tabs() {
	echo '<!-- Start of pcp_equalizer devices_tabs toolbar -->'
	echo '<p style="margin-top:8px;">'

	for j in $EQUALDEVICES; do
		[ "$j" = "$CUR_EQUAL_DEVICE" ] && TAB_STYLE="tab7a" || TAB_STYLE="tab7"
		echo '  <a class="'$TAB_STYLE'" href="'$0'?CUR_EQUAL_DEVICE='$j'" title="'$j'">'$j'</a>'
	done

	echo '</p>'
	echo '<div class="tab7end" style="margin-bottom:10px;">pCP</div>'
	echo '<!-- End of pcp_equalizer devices toolbar -->'
}

if [ -f /home/tc/.alsaequal.presets ]; then
	PRESETS=1
	. /home/tc/.alsaequal.presets
	PRESET_NAMES=$(cat /home/tc/.alsaequal.presets | awk -F= '{print $1}')
fi

case "$ACTION" in
	Test)
		RANGE="$R1 $R2 $R3 $R4 $R5 $R6 $R7 $R8 $R9 $R10"
	;;
	Save)
		RANGE="$R1 $R2 $R3 $R4 $R5 $R6 $R7 $R8 $R9 $R10"
		pcp_backup >/dev/null 2>&1
	;;
	Reset)
		RANGE="66 66 66 66 66 66 66 66 66 66"
	;;
esac

for VALUE in $RANGE
do
	${SET_EQUAL}$BAND $VALUE >/dev/null 2>&1
	BAND=$((BAND+1))
done

# Determine if ALSA equalizer is loaded
CURRENT_EQ_SETTINGS=$(sudo amixer -D $CUR_EQUAL_DEVICE contents | grep ": values" | awk -F"," '{print $2}')

pcp_debug_variables "html" ACTION CUR_EQUAL_DEVICE CURRENT_EQ_SETTINGS RANGE SET_EQUAL

if [ x"" = x"$CURRENT_EQ_SETTINGS" ]; then
	pcp_infobox_begin "" "html"
	pcp_message ERROR "ALSA Equalizer is not loaded." "html"
	pcp_message INFO "Load ALSA Equalizer from the [Tweaks] page." "html"
	pcp_infobox_end
	pcp_html_end
	exit
fi

pcp_equal_devices_tabs

#-----------------------------Manual Equalizer Adjustment--------------------------------


pcp_heading5 "Manual Equalizer Adjustment for '$CUR_EQUAL_DEVICE'"
echo '            <form name="manual_adjust" action="'$0'" method="get">'
#----------------------------------------------------------------------------------------
for VALUE in $CURRENT_EQ_SETTINGS
do
	echo '              <div class="row">'
	echo '                <div class="col-6">'
	echo '                  <output name="P'$i'" id="P'$i'" for="R'$i'">'$VALUE'</output>'
	echo '                </div>'
	echo '                <div>'
	echo '                  <p style="height:12px">'
	echo '                    <input class="large36"'
	echo '                           type="range"'
	echo '                           id="R'$i'"'
	echo '                           name="R'$i'"'
	echo '                           value="'$VALUE'"'
	echo '                           min="0"'
	echo '                           max="100"'
	echo '                           oninput="P'$i'.value=R'$i'.value"'
	echo '                    >&nbsp;&nbsp;&nbsp;'$(eval "echo \$LB$i")
	echo '                  </p>'
	echo '                </div>'
	echo '              </div>'
	i=$((i+1))
done
#----------------------------------------------------------------------------------------
echo '              <div class="row">'
echo '                <div class="col-2">'
echo '                  <input type="hidden" name="CUR_EQUAL_DEVICE" value="'$CUR_EQUAL_DEVICE'">'
echo '                </div>'
echo '                <div class="col-2">'
echo '                  <input type="submit" name="ACTION" value="Save">'
echo '                </div>'
echo '                <div class="col-2">'
echo '                  <input type="submit" name="ACTION" value="Reset">'
echo '                </div>'
echo '                <div class="col-2">'
echo '                  <input type="submit" name="ACTION" value="Test">'
echo '                </div>'
echo '              </div>'
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '              <div class="row">'
echo '                <div>'
echo '                  <p><b>10-band equalizer&nbsp;&nbsp;</b>'
echo '                    <a id="dt'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '                    <p>Use the sliders to adjust the soundstage, then</p>'
echo '                    <ul>'
echo '                      <li><b>Save</b> - The equalizer settings are saved to make them available after a reboot.</li>'
echo '                      <li><b>Test</b> - The changes will be written to ALSA, so you can hear the effects.</li>'
echo '                      <li><b>Reset</b> - Set the equalizer to the defaults settings.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </div>'
echo '              </div>'
#----------------------------------------------------------------------------------------
echo '            </form>'
echo '      </div>'
#----------------------------------------------------------------------------------------

#--------------------------------------Presets-------------------------------------------
if [ $PRESETS -eq 1 ]; then

	echo '      <div class="row">'
	pcp_heading5 "Presets"
	echo '            <form name="presets" action="'$0'" method="get">'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	echo '              <div class="row">'
	echo '                <div class="XXXX">'
	echo '                  <p>Preset</p>'
	echo '                </div>'
	echo '                <div class="XXXX">'
	echo '                  <select class="large16" name="RANGE">'

	for VALUE in $PRESET_NAMES
	do
		echo '                    <option value="'$(eval "echo \$$VALUE")'">'$VALUE'</option>'
	done

	echo '                  </select>'
	echo '                </div>'
	echo '                <div>'
	echo '                  <p>Select one of your presets&nbsp;&nbsp;</b>'
	echo '                    <a id="dt'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '                    <p>Use [Save] and [Test] after selecting preset to make it permanent.</p>'
	echo '                    <p>Presets are:</p>'
	echo '                    <ul>'
	echo '                      <li>An advanced feature that requires some Linux skills to maintain.</li>'
	echo '                      <li>Stored in the file $HOME/.alsaequal.presets</li>'
	echo '                      <li>Edited using a text editor such as vi.</li>'
	echo '                      <li>The format of the presets file is important, i.e.</li>'
	echo '                      <ul>'
	echo '                        <li>RESET="66 66 66 66 66 66 66 66 66 66"</li>'
	echo '                        <li>The name of the preset is a simple single word, no spaces.</li>'
	echo '                        <li>There are 10 values between 0 and 100, enclosed in double quotes.</li>'
	echo '                      </ul>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </div>'
	echo '              </div>'
	#------------------------------------------------------------------------------------
	echo '              <div class="row">'
	echo '                <div class="XXXX">'
	echo '                  <input type="hidden" name="CUR_EQUAL_DEVICE" value="'$CUR_EQUAL_DEVICE'">'
	echo '                  <input type="submit" name="ACTION" value="Use Preset">'
	echo '                </div>'
	echo '              </div>'
	#------------------------------------------------------------------------------------
	echo '            </form>'
	echo '      </div>'

fi
#----------------------------------------------------------------------------------------

pcp_html_end