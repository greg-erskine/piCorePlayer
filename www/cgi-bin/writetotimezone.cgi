#!/bin/sh

# Version: 0.04 2015-06-25 SBP
#	Removed reboot button - not needed anymore.

# Version: 0.03 2015-05-10 SBP
#	Fixed the saving command so that slashes are saved as well.

# Version: 0.03 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.02 2014-09-04 GE
#	Moved code to pcp_set_timezone routine.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables

pcp_html_head "Set Timezone" "GE" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string
pcp_save_to_config

echo '<p class="info">[ INFO ] Timezone: '$TIMEZONE'</p>'

pcp_mount_mmcblk0p1
pcp_set_timezone
pcp_umount_mmcblk0p1

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Local time: '$(date)'</p>'

pcp_backup
pcp_go_back_button

echo '</body>'
echo '</html>'