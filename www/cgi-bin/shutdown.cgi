#!/bin/sh
. pcp-functions
pcp_variables

# Version: 0.02 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.01 2014-06-24 GE
#	Original.

pcp_html_head "Shutdown Raspberry Pi" "SBP" "5" "main.cgi"

pcp_banner
pcp_running_script
pcp_shutdown

echo '</body>'
echo '</html>'