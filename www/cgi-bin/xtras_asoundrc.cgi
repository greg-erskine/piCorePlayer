#!/bin/sh

# Version: 0.02 2015-04-25 GE
#   Continued development.

# Version: 0.01 2015-03-10 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_asound_conf" "GE"

pcp_controls
pcp_banner
pcp_xtras
pcp_mode_lt_99
pcp_running_script

DEBUG=0                 # <--- LOOK
MODE=0                  # <--- LOOK
VOLUMERIGHT=100
VOLUMELEFT=100

#========================================================================================
# Write asound.conf - 0 = left, 1 = right
#----------------------------------------------------------------------------------------
pcp_write_asound_conf() {
	echo '# '$OPTION' - Generated by piCorePlayer' >$ASOUNDCONF
	echo 'pcm.!default {'                         >>$ASOUNDCONF
	echo '	type route'                           >>$ASOUNDCONF
	echo '	slave.pcm hw'                         >>$ASOUNDCONF
                                                 
	case $OPTION in                              
		stereo)                                  
			echo '	ttable {'                     >>$ASOUNDCONF
			echo '		0.0 '$VOLLEFT             >>$ASOUNDCONF
			echo '		1.1 '$VOLRIGHT            >>$ASOUNDCONF
			echo '	}'                            >>$ASOUNDCONF
			;;                                   
		mono)                                    
			echo '	ttable {'                     >>$ASOUNDCONF
			echo '		0.1 '$VOLLEFT             >>$ASOUNDCONF
			echo '		0.0 '$VOLLEFT             >>$ASOUNDCONF
			echo '		1.0 '$VOLRIGHT            >>$ASOUNDCONF
			echo '		1.1 '$VOLRIGHT            >>$ASOUNDCONF
			echo '	}'                            >>$ASOUNDCONF
			;;                                   
		swap)                                    
			echo '	ttable {'                     >>$ASOUNDCONF
			echo '		0.1 '$VOLLEFT             >>$ASOUNDCONF
			echo '		1.0 '$VOLRIGHT            >>$ASOUNDCONF
			echo '	}'                            >>$ASOUNDCONF
			;;                                   
		left)                                    
			echo '	ttable {'                     >>$ASOUNDCONF
			echo '		0.0 '$VOLLEFT             >>$ASOUNDCONF
			echo '		1.1 0'                    >>$ASOUNDCONF
			echo '	}'                            >>$ASOUNDCONF
			;;                                   
		right)                                   
			echo '	ttable {'                     >>$ASOUNDCONF
			echo '		0.0 0'                    >>$ASOUNDCONF
			echo '		1.1 '$VOLRIGHT            >>$ASOUNDCONF
			echo '	}'                            >>$ASOUNDCONF
			;;                                   
	esac                                         
	echo '}'                                      >>$ASOUNDCONF
}

pcp_httpd_query_string

VOLLEFT="0."$VOLUMELEFT
if [ $VOLUMELEFT -eq 0 ]; then
	VOLLEFT=0
elif [ $VOLUMELEFT -lt 10 ]; then
	VOLLEFT="0.0"$VOLUMELEFT
elif [ $VOLUMELEFT -ge 100 ]; then
	VOLLEFT=1
fi

VOLRIGHT="0."$VOLUMERIGHT
if [ $VOLUMERIGHT -eq 0 ]; then
	VOLRIGHT=0
elif [ $VOLUMERIGHT -lt 10 ]; then
	VOLRIGHT="0.0"$VOLUMERIGHT
elif [ $VOLUMERIGHT -ge 100 ]; then
	VOLRIGHT=1
fi

case "$SUBMIT" in
	Write)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Writing asound.conf...</p>'
		pcp_write_asound_conf
		;;
	*)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Invalid option '$SUBMIT'...</p>'
		;;
esac

TYPE=$(cat $ASOUNDCONF)
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Type '${TYPE:2:3}'</p>'
case ${TYPE:2:3} in
	ste) STE="checked" ;;
	mon) MON="checked" ;;
	swa) SWA="checked" ;;
	lef) LEF="checked" ;;
	rig) RIG="checked" ;;
	*)   STE="checked" ;;
esac

#========================================================================================
# Start table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="asound" action="xtras_asoundrc.cgi" method="get" id="asound">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Generate asound.conf</legend>'
echo '            <table class="bggrey percent100">'

echo '              <tr class="even">'
echo '                <td class="column150">'
echo '                  <p class="row">Stereo/Mono/Swap/L/R</p>'
echo '                </td>'
echo '                <td class="column410">'
echo '                  <input class="small1" type="radio" name="OPTION" id="ASOUND" value="stereo" '$STE'>Stereo&nbsp;'
echo '                  <input class="small1" type="radio" name="OPTION" id="ASOUND" value="mono" '$MON'>Mono&nbsp;'
echo '                  <input class="small1" type="radio" name="OPTION" id="ASOUND" value="swap" '$SWA'>Swap channels&nbsp;'
echo '                  <input class="small1" type="radio" name="OPTION" id="ASOUND" value="left" '$LEF'>Left channel&nbsp;'
echo '                  <input class="small1" type="radio" name="OPTION" id="ASOUND" value="right" '$RIG'>Right channel'
echo '                </td>'
echo '                <td>'
echo '                  <p class="row"></p>'
echo '                </td>'
echo '              </tr>'

echo '              <tr class="odd">'
echo '                <td class="column150">'
echo '                  <p class="row">Left channel</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="small2" type="text" id="VOLUMELEFT" name="VOLUMELEFT" value="'$VOLUMELEFT'">&nbsp;Volume (1-100)'
echo '                </td>'
echo '                <td class="column150">'
echo '                  <p class="row"></p>'
echo '                </td>'
echo '              </tr>'

echo '              <tr class="even">'
echo '                <td class="column150">'
echo '                  <p class="row">Right channel</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="small2" type="text" id="VOLUMERIGHT" name="VOLUMERIGHT" value="'$VOLUMERIGHT'">&nbsp;Volume (1-100)'
echo '                </td>'
echo '                <td class="column150">'
echo '                  <p class="row"></p>'
echo '                </td>'
echo '              </tr>'

echo '              </tr>'
echo '              <tr>'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="SUBMIT" value="Write">'
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
# Current asound.conf
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
if [ $MODE = 99 ]; then
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="asound_conf" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Current asound.conf</legend>'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="odd">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "cat $ASOUNDCONF" 150
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
fi
echo '  <tr class="odd">'
echo '    <td class="column150 center">'
echo '      <form id="Restart" name="Restart" action="restartsqlt.cgi" method="get">'
echo '        <input type="submit" value="Restart" />'
echo '      </form>'
echo '    </td>'
echo '    <td colspan="2">'
echo '      <p class="row">Restart Squeezelite - necessary for new asound.conf to take effect.</p>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'