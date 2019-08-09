#!/bin/sh

# Version: 6.0.0 2019-08-10

. pcp-functions

pcp_html_head "xtras copy2fs" "GE"

pcp_banner
pcp_xtras
pcp_httpd_query_string

REBOOT_REQUIRED=false

#----------------------------------------------------------------------------------------
# copy2fs actions
#----------------------------------------------------------------------------------------
case "$COPY2FS" in
	yes)
		touch ${TCEMNT}/tce/copy2fs.flg
		REBOOT_REQUIRED=true
	;;
	no)
		rm -f ${TCEMNT}/tce/copy2fs.flg
		REBOOT_REQUIRED=true
	;;
esac

#========================================================================================
# copy2fs table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="copy2fs" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>copy2fs</legend>'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
[ -f ${TCEMNT}/tce/copy2fs.flg ] && COPY2FSyes="checked" || COPY2FSno="checked"

pcp_start_row_shade
pcp_incr_id
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>copy2fs flag set</p>'
echo '                </td>'
echo '                <td class="column150">'
echo '                  <input class="small1" type="radio" name="COPY2FS" value="yes" '$COPY2FSyes'>Yes'
echo '                  <input class="small1" type="radio" name="COPY2FS" value="no" '$COPY2FSno'>No'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set the copy2fs flag&nbsp;&nbsp;'
echo '                  <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a></p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>This sets the copy2fs flag so, on the next reboot, all extensions are loaded into RAM.</p>'
echo '                    <p>A reboot is required for the copy2fs flag to take effect.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
# Mounted filesystems table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Current mounted filesystems</legend>'
echo '          <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
                      pcp_textarea_inform "none" "df" 200
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>Example: copy2fs not set</b></p>'
echo '                <p>Note: There will be lots of loop mounted filesystems, one for each extension.</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo                  '<textarea class="inform" style="height:160px">'
echo                    'Filesystem           1K-blocks      Used Available Use% Mounted on'
echo                    'tmpfs                   222492         0    222492   0% /dev/shm'
echo                    '/dev/mmcblk0p2           36561     15244     18379  45% /mnt/mmcblk0p2'
echo                    '/dev/loop0                 128       128         0 100% /tmp/tcloop/pcp'
echo                    '/dev/loop1                 128       128         0 100% /tmp/tcloop/pcp-base'
echo                    '/dev/loop2                 128       128         0 100% /tmp/tcloop/alsa'
echo                    '/dev/loop3                1152      1152         0 100% /tmp/tcloop/alsa-utils'
echo                    '/dev/loop4                 128       128         0 100% /tmp/tcloop/busybox-httpd'
echo                    '     .                      .         .          .   .          .'
echo                    '     .                      .         .          .   .          .'
echo                  '</textarea>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>Example: copy2fs set</b></p>'
echo '                <p>Note: There are no loop mounted filesystems.</p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
#----------------------------------------------------------------------------------------
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo                  '<textarea class="inform" style="height:60px">'
echo                    'Filesystem           1K-blocks      Used Available Use% Mounted on'
echo                    'tmpfs                   222492         0    222492   0% /dev/shm'
echo                    '/dev/mmcblk0p2           36561     15244     18379  45% /mnt/mmcblk0p2'
echo                  '</textarea>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'

$REBOOT_REQUIRED
[ $? -eq 0 ] && pcp_reboot_required
exit
