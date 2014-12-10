#!/bin/sh
. pcp-functions
pcp_variables

# Version: 0.02 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.01 2014-06-24 GE
#	Original.

pcp_html_head "Restart Squeezelite" "SBP" "5" "main.cgi"

pcp_banner
pcp_running_script
pcp_squeezelite_stop
sleep 2
pcp_squeezelite_start

echo '</body>'
echo '</html>'