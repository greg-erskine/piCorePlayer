#!/bin/sh

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

# Save the encoded parameter to the config file, with quotes
sudo sed -i "s/\(TIMEZONE=\).*/\1\"$TIMEZONE\"/" $CONFIGCFG

# Decode variables using httpd, no quotes
TIMEZONE=`sudo /usr/local/sbin/httpd -d $TIMEZONE`

echo '<p class="info">[ INFO ] Timezone: '$TIMEZONE'</p>'

pcp_set_timezone

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Local time:  '$(date)'</p>'

pcp_backup
echo '<p class="info">[ INFO ] Reboot is required to set timezone.</p>'
pcp_reboot_button
pcp_go_back_button

echo '</body>'
echo '</html>'