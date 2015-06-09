#!/bin/sh

# Version: 0.06 2014-12-11 GE
#	HTML5 formatting.

# Version: 0.05 2014-xx-xx SBP
#	Added support for the HiFiBerry AMP.

# Version: 0.04 2014-10-24 GE
#	Added textareas.
#	Using pcp_html_head now.
#	Minor tidyup.

# Version: 0.03 2014-09-25 SBP
#	Added support for the hifiberry DAC+ and Digi+.
#   Added support for the IQaudIO+ DAC.

# Version: 0.02 2014-08-08 GE
#	Major clean up.

# Version: 0.01 SBP
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Choose output" "SBP" "10" "squeezelite.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Decode variables using httpd, add quotes
AUDIO=`sudo $HTPPD -d \"$AUDIO\"`

# Save variable $AUDIO to the config file
sudo sed -i "s/\(AUDIO *=*\).*/\1$AUDIO/" $CONFIGCFG

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] QUERY_STRING: '$QUERY_STRING'<br />'
	echo '                 [ DEBUG ] AUDIO: '$AUDIO'<br />'
	echo '                 [ DEBUG ] OUTPUT: '$OUTPUT'</p>'
fi

pcp_squeezelite_stop

# Set the default settings
case "$AUDIO" in
	\"Analog*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		echo '<textarea class="white" style="height: 130px;" >'
			pcp_disable_i2s
			sudo ./disablehdmi.sh
		echo '</textarea>'
		OUTPUT="sysdefault:CARD=ALSA"
		ALSA_PARAMS="80:::0"
		;;
	\"HDMI*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		echo '<textarea class="white" style="height: 130px;" >'
			pcp_disable_i2s
			sudo ./enablehdmi.sh
		echo '</textarea>'
		OUTPUT="sysdefault:CARD=ALSA"
		ALSA_PARAMS="::32:0"
		;;
	\"USB*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		echo '<textarea class="white" style="height: 130px;" >'
			pcp_disable_i2s
			sudo ./disablehdmi.sh
		echo '</textarea>'
		OUTPUT=" "
		ALSA_PARAMS="80:4::"
		;;
	\"I2SDAC*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		echo '<textarea class="white" style="height: 130px;" >'
			pcp_enable_i2s_dac
			sudo ./disablehdmi.sh
		echo '</textarea>'
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		;;
	\"I2SDIG*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		echo '<textarea class="white" style="height: 130px;" >'
			pcp_enable_i2s_digi
			sudo ./disablehdmi.sh
		echo '</textarea>'
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		;;
	\"I2SAMP*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		echo '<textarea class="white" style="height: 130px;" >'
			pcp_enable_i2s_amp
			sudo ./disablehdmi.sh
		echo '</textarea>'
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		;;
	\"IQaudio*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		echo '<textarea class="white" style="height: 130px;" >'
			pcp_enable_iqaudio_dac
			sudo ./disablehdmi.sh
		echo '</textarea>'
		OUTPUT="hw:CARD=IQaudIODAC"
		ALSA_PARAMS="80:4::"
		;;
	\"I2SpDAC*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		echo '<textarea class="white" style="height: 130px;" >'
			sudo ./disablehdmi.sh
			pcp_enable_hifiberry_dac_p
					echo '</textarea>'
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		;;	
	\"I2SpDIG*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		echo '<textarea class="white" style="height: 130px;" >'
			pcp_enable_i2s_digi
			sudo ./disablehdmi.sh
		echo '</textarea>'
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		;;
	\"I2SpIQaudIO*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		echo '<textarea class="white" style="height: 130px;" >'
			pcp_enable_iqaudio_dac
			sudo ./disablehdmi.sh
		echo '</textarea>'
		OUTPUT="hw:CARD=IQaudIODAC"
		ALSA_PARAMS="80:4::"
		;;
	*)
		echo '<p class="error">[ ERROR ] Error setting '$AUDIO'</p>'
		;;
esac
pcp_save_to_config

pcp_squeezelite_start

pcp_show_config_cfg
pcp_backup
pcp_go_back_button

echo '</body>'
echo '</html>'