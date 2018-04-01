#!/bin/sh

# Version: 3.5.1 2018-04-02
#	Added pcp_redirect_button. GE.
#	HTML5 cleanup. GE.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.

# Version: 0.01 2014-06-24 GE
#	Original. GE.

. pcp-functions

pcp_html_head "Shutdown Raspberry Pi" "SBP"

pcp_banner
pcp_running_script

pcp_table_top "Shutdowning piCorePlayer"
pcp_shutdown
pcp_table_middle
pcp_redirect_button "Go to Main Page" "main.cgi" 5
pcp_table_end

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'