#!/bin/sh

# Version: 5.1.0 2019-06-29

. pcp-functions
. pcp-lms-functions

pcp_html_head "LMS CLI test" "GE"

pcp_banner
pcp_xtras
pcp_httpd_query_string

if [ $DEBUG -eq 1 ]; then
	echo '<p class="debug">[ DEBUG ] LMS IP: '$(pcp_lmsip)'<br />'
	echo '                 [ DEBUG ] MAC: '$(pcp_controls_mac_address)'</p>'
fi

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Select LMS</legend>'
echo '          <form name="new-lms-ip" action="'$0'" method="get">'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150 center">'
echo '                  <input type="submit" name="SUBMIT" value="Connect">'
echo '                </td>'
echo '                <td class="column210">'

if which find_servers >/dev/null 2>&1; then
	echo '                  <select class="large16" name="NEWLMSIP">'
	find_servers | sed -e 's|(||' -e 's|)||' | awk '{ printf "<option value=%s>%s</option>\n", $2, $1 }'
	echo '                  </select>'
else
	echo ' <p class="error">[ ERROR ] find_servers missing.</p>'
fi

echo '                </td>'
echo '                <td>'
echo '                  <p>Connect to LMS&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>This will connect piCorePlayer to selected LMS.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </form>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

[ "$SUBMIT" = "Connect" ] && pcp_lms_connect "$NEWLMSIP"

#========================================================================================
pcp_table_top "Testing the functions in pcp-lms-functions"
#----------------------------------------------------------------------------------------

#--------------------------------------pcp_lms_players-----------------------------------
echo '<h2>Squeezelite players: (pcp_lms_players squeezelite)</h2>'
PLAYERDATA=$(pcp_lms_players squeezelite)
echo '<p>'$PLAYERDATA'</p>'

PLAYERS=$(echo "$PLAYERDATA" | awk -F",1 " '{ for(i=1;i<=NF;i++) { printf "<p>%s</p>%s", $i, "\n"} }')
echo $PLAYERS

#--------------------------------------pcp_lms_player_status-----------------------------
echo '<h2>Status: (pcp_lms_player_status)</h2>'
echo '<p>'$(pcp_lms_player_status)'</p>'

#--------------------------------------pcp_lms_artists-----------------------------------
echo '<h2>Artists: (pcp_lms_artists)</h2>'
echo '<p><b>Note:</b> Limited to first 20 artists.</p>'
echo '<p>'$(pcp_lms_artists 20)'</p>'
echo '<br />'

#--------------------------------------pcp_lms_mode--------------------------------------
echo '<h2>Mode: (pcp_lms_mode)</h2>'
echo '<p>'$(pcp_lms_mode)'</p>'

#--------------------------------------pcp_lms_time--------------------------------------
echo '<h2>Time: (pcp_lms_time)</h2>'
echo '<p>'$(pcp_lms_time)'</p>'

#--------------------------------------pcp_lms_genre--------------------------------------
echo '<h2>Genre: (pcp_lms_genre)</h2>'
echo '<p>'$(pcp_lms_genre)'</p>'

#--------------------------------------pcp_lms_artist------------------------------------
echo '<h2>Artist: (pcp_lms_artist)</h2>'
echo '<p>'$(pcp_lms_artist)'</p>'

#--------------------------------------pcp_lms_album-------------------------------------
echo '<h2>Album: (pcp_lms_album)</h2>'
echo '<p>'$(pcp_lms_album)'</p>'

#--------------------------------------pcp_lms_title-------------------------------------
echo '<h2>Title: (pcp_lms_title)</h2>'
echo '<p>'$(pcp_lms_title)'</p>'

#--------------------------------------pcp_lms_duration----------------------------------
echo '<h2>Duration: (pcp_lms_duration)</h2>'
echo '<p>'$(pcp_lms_duration)'</p>'

#--------------------------------------pcp_lms_remote------------------------------------
echo '<h2>Remote: (pcp_lms_remote)</h2>'
echo '<p>'$(pcp_lms_remote)'</p>'

#--------------------------------------pcp_lms_current_title-----------------------------
echo '<h2>Current_title: (pcp_lms_current_title)</h2>'
echo '<p>'$(pcp_lms_current_title)'</p>'

#--------------------------------------pcp_lms_path--------------------------------------
echo '<h2>Path: (pcp_lms_path)</h2>'
echo '<p>'$(pcp_lms_path)'</p>'

#--------------------------------------pcp_lms_player_count------------------------------
echo '<h2>Player count: (pcp_lms_player_count)</h2>'
echo '<p>'$(pcp_lms_player_count)'</p>'

#--------------------------------------pcp_lms_player_id---------------------------------
echo '<h2>Player id: (pcp_lms_player_id)</h2>'
echo '<p>'$(pcp_lms_player_id)'</p>'

#--------------------------------------pcp_lms_player_uuid-------------------------------
echo '<h2>Player uuid: (pcp_lms_player_uuid)</h2>'
echo '<p>'$(pcp_lms_player_uuid)'</p>'

#--------------------------------------pcp_lms_player_name-------------------------------
echo '<h2>Player name: (pcp_lms_player_name)</h2>'
echo '<p>'$(pcp_lms_player_name)'</p>'

#--------------------------------------pcp_lms_player_ip---------------------------------
echo '<h2>Player ip: (pcp_lms_player_ip)</h2>'
echo '<p>'$(pcp_lms_player_ip)'</p>'

#--------------------------------------pcp_lms_player_model------------------------------
echo '<h2>Player model: (pcp_lms_player_model)</h2>'
echo '<p>'$(pcp_lms_player_model)'</p>'

#--------------------------------------pcp_lms_player_isplayer---------------------------
echo '<h2>Player isplayer: (pcp_lms_player_isplayer)</h2>'
echo '<p>'$(pcp_lms_player_isplayer)'</p>'

#--------------------------------------pcp_lms_player_displaytype------------------------
echo '<h2>Player displaytype: (pcp_lms_player_displaytype)</h2>'
echo '<p>'$(pcp_lms_player_displaytype)'</p>'

#--------------------------------------pcp_lms_player_canpoweroff------------------------
echo '<h2>Player canpoweroff: (pcp_lms_player_canpoweroff)</h2>'
echo '<p>'$(pcp_lms_player_canpoweroff)'</p>'

#--------------------------------------pcp_lms_signalstrength----------------------------
echo '<h2>Signalstrength: (pcp_lms_signalstrength)</h2>'
echo '<p>'$(pcp_lms_signalstrength)'</p>'

#--------------------------------------pcp_lms_name--------------------------------------
echo '<h2>Name: (pcp_lms_name)</h2>'
echo '<p>'$(pcp_lms_name)'</p>'

#--------------------------------------pcp_lms_connected---------------------------------
echo '<h2>Connected: (pcp_lms_connected)</h2>'
echo '<p>'$(pcp_lms_connected)'</p>'

#--------------------------------------pcp_lms_info_total_genres-------------------------
echo '<h2>info_total_genres: (pcp_lms_info_total_genres)</h2>'
echo '<p>'$(pcp_lms_info_total_genres)'</p>'

#--------------------------------------pcp_lms_info_total_artists------------------------
echo '<h2>info_total_artists: (pcp_lms_info_total_artists)</h2>'
echo '<p>'$(pcp_lms_info_total_artists)'</p>'

#--------------------------------------pcp_lms_info_total_albums-------------------------
echo '<h2>info_total_albums: (pcp_lms_info_total_albums)</h2>'
echo '<p>'$(pcp_lms_info_total_albums)'</p>'

#--------------------------------------pcp_lms_info_total_songs--------------------------
echo '<h2>info_total_songs: (pcp_lms_info_total_songs)</h2>'
echo '<p>'$(pcp_lms_info_total_songs)'</p>'

#--------------------------------------pcp_lms_show--------------------------------------
echo '<h2>Show: (pcp_lms_show)</h2>'
echo '<p>'$(pcp_lms_show)'</p>'

#===============================================================

[ x"" = x"$LMSWEBPORT" ] && LMSPORT=9000 || LMSPORT=$LMSWEBPORT
echo '<br />'
echo '<div>'
echo '<img src="http://'$(pcp_lmsip)':'${LMSPORT}$(pcp_lms_show)'" alt="Currently playing" style="height:250px; width:250px; border:1px solid black;"/>'
echo '</div>'
echo '<br />'

pcp_table_end

pcp_footer
pcp_copyright
echo '</body>'
echo '</html>'
exit
