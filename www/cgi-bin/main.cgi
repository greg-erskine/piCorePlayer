#!/bin/sh

# Version: 0.08 2014-12-08 SBP
#	Revised button order.
#	Added Squeezelite running indicator.
#	Reformatted.

# Version: 0.07 2014-10-22 GE
#	Using pcp_html_head now.

# Version: 0.06 2014-10-09 GE
#	Revised uptime delay to use seconds.

# Version: 0.05 2014-10-08 GE
#	Size of input buttons controlled through input[type=submit] style.

# Version: 0.04 2014-10-02 GE
#	Added uptime delay before pcp_squeezelite_status is checked.

# Version: 0.03 2014-09-20 GE
#	Modified HTML to improve cross browser support.

# Version: 0.02 2014-08-22 GE
#	Added check for pcp_squeezelite_status.

# Version: 0.01 2014-06-25 GE
#	Original.

. pcp-functions
pcp_variables

pcp_html_head "Main Page" "SBP"

pcp_controls
pcp_banner
pcp_navigation

#[ $(pcp_uptime_seconds) -gt 60 ] && [ $(pcp_squeezelite_status) = 1 ] &&
#echo '<p class="error">[ ERROR ] Squeezelite not running.</p>'

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] System uptime (sec): '$(pcp_uptime_seconds)'<br />'
	echo '                 [ DEBUG ] System uptime (min): '$(pcp_uptime_minutes)'<br />'
	echo '                 [ DEBUG ] Squeezelite status: '$(pcp_squeezelite_status)'</p>'
fi

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '      <fieldset>'
echo '        <legend>Change Squeezelite settings</legend>'

echo '<table class="bggrey percent100">'

#------------------------------------------Squeezelite Indication------------------------
echo '  <tr class="even">'
echo '    <td>'

if [ $(pcp_squeezelite_status) = 0 ]; then
     echo '      <div class="circle" style="background-color:green;"></div>'
     echo '    </td>'
     echo '    <td>'
     echo '      <p>Squeezelite is running.</p>'
     echo '    </td>'
else 
     echo '      <div class="circle" style="background-color:red;"></div>'
     echo '    </td>'
     echo '    <td>'
     echo '      <p>Squeezelite is not running.</p>'
     echo '    </td>'
 fi
 
 echo '  </tr>'

#------------------------------------------Padding---------------------------------------
echo '  <tr height="8">'
echo '    <td></td>'
echo '    <td></td>'
echo '  </tr>'

#------------------------------------------Stop------------------------------------------
echo '  <tr class="even">'
echo '    <td>'
echo '      <form name="Stop" action="stop.cgi" method="get" id="Stop">'
echo '        <input type="submit" value="Stop" />'
echo '      </form>'
echo '    </td>'
echo '    <td>'
echo '      <p>Stop Squeezelite.</p>'
echo '    </td>'
echo '  </tr>'

#------------------------------------------Restart---------------------------------------
echo '  <tr class="odd">'
echo '    <td>'
echo '      <form name="Restart" action="restartsqlt.cgi" method="get" id="Restart">'
echo '        <input type="submit" value="Restart" />'
echo '      </form>'
echo '    </td>'
echo '    <td>'
echo '      <p>Restart Squeezelite with new settings.</p>'
echo '    </td>'
echo '  </tr>'

#------------------------------------------Update Squeezelite - Triode-------------------
echo '  <tr class="even">'
echo '    <td>'
echo '      <form name="updateTriode" action="updatesqlt.cgi" method="get" id="updateTriode">'
echo '        <input type="hidden" name="VERSION" value="Triode"/>'
echo '        <input type="submit" value="Update" />'
echo '      </form>'
echo '    </td>'
echo '    <td>'
echo '      <p>Triode'\''s newest version. Download and update Squeezelite.</p>'
echo '    </td>'
echo '  </tr>'

#------------------------------------------Update Squeezelite - Ralphy-------------------
echo '  <tr class="odd">'
echo '    <td>'
echo '      <form name="updateRalphy" action="updatesqlt.cgi" method="get" id="updateRalphy">'
echo '        <input type="hidden" name="VERSION" value="Ralphy"/>'
echo '        <input type="submit" value="Update" />'
echo '      </form>'
echo '    </td>'
echo '    <td>'
echo '      <p>Ralphy'\''s newest version. Download and update Squeezelite. This one allows upsampling using SOX and can play wma and alac via ffmpeg.</p>'
echo '    </td>'
echo '  </tr>'

#------------------------------------------Backup----------------------------------------
echo '  <tr class="even">'
echo '    <td>'
echo '      <form name="backup" action="javascript:pcp_confirm('\''Do a backup?'\'','\''backup.cgi'\'')" method="get" id="backup">'
echo '        <input type="submit" value="Backup" />'
echo '      </form>'
echo '    </td>'
echo '    <td>'
echo '      <p>Backup your changes.</p>'
echo '    </td>'
echo '  </tr>'

#------------------------------------------Reboot----------------------------------------
echo '  <tr class="odd">'
echo '    <td>'
echo '      <form name="Reboot" action="javascript:pcp_confirm('\''Reboot piCorePlayer?'\'','\''reboot.cgi'\'')" method="get" id="Reboot">'
echo '        <input type="submit" value="Reboot" />'
echo '      </form>'
echo '    </td>'
echo '    <td>'
echo '      <p>Reboot - necessary if you are enabling or disabling HDMI output.</p>'
echo '    </td>'
echo '  </tr>'

#------------------------------------------Shutdown--------------------------------------
echo '  <tr class="even">'
echo '    <td>'
echo '      <form name="Shutdown" action="javascript:pcp_confirm('\''Shutdown piCorePlayer?'\'','\''shutdown.cgi'\'')" method="get" id="Shutdown">'
echo '        <input type="submit" value="Shutdown" />'
echo '      </form>'
echo '    </td>'
echo '    <td>'
echo '      <p>Shutdown - Put your Raspberry Pi to sleep.</p>'
echo '    </td>'
echo '  </tr>'

#------------------------------------------Update pCP------------------------------------
echo '  <tr class="odd">'
echo '    <td>'
echo '      <form name="InSitu" action="upd_picoreplayer.cgi" method="get" id="InSitu">'
echo '        <input type="submit" value="Update pCP" />'
echo '      </form>'
echo '    </td>'
echo '    <td>'
echo '      <p>Update piCorePlayer without removing the SD-card.</p>'
echo '    </td>'
echo '  </tr>'

#------------------------------------------Save to USB-----------------------------------
echo '  <tr class="even">'
echo '    <td>'
echo '      <form name="Saveconfig" action="save2usb.cgi" method="get" id="Saveconfig">'
echo '        <input type="submit" value="Save to USB" />'
echo '      </form>'
echo '    </td>'
echo '    <td>'
echo '      <p>Save your current configuration to USB stick for use after update or to be used in another piCorePlayer.</p>'
echo '    </td>'
echo '  </tr>'

echo '</table>'

#----------------------------------------------------------------------------------------
echo '      </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

pcp_footer

echo '</body>'
echo '</html>'