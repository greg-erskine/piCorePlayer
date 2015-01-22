#!/bin/sh

# Version: 0.04 2015-01-22 SBP
#	Added CLOSEOUT.
#	Removed debugging code.

# Version: 0.03 2014-12-12 GE
#	HTML5 format.
#	Minor mods.

# Version: 0.02 2014-08-22 SBP
#	Changed the back button to absolute path back to Squeezelite.cgi. Otherwise we would go in circles.

# Version: 0.01 2014-06-25 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write Write to config.cfg" "SBP" "15" "squeezelite.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Decode variables using httpd, add quotes
NAME=`sudo /usr/local/sbin/httpd -d \"$NAME\"`
OUTPUT=`sudo /usr/local/sbin/httpd -d \"$OUTPUT\"`
ALSA_PARAMS=`sudo /usr/local/sbin/httpd -d \"$ALSA_PARAMS\"`
BUFFER_SIZE=`sudo /usr/local/sbin/httpd -d \"$BUFFER_SIZE\"`
_CODEC=`sudo /usr/local/sbin/httpd -d \"$_CODEC\"`
PRIORITY=`sudo /usr/local/sbin/httpd -d \"$PRIORITY\"`
MAX_RATE=`sudo /usr/local/sbin/httpd -d \"$MAX_RATE\"`
UPSAMPLE=`sudo /usr/local/sbin/httpd -d \"$UPSAMPLE\"`
MAC_ADDRESS=`sudo /usr/local/sbin/httpd -d \"$MAC_ADDRESS\"`
SERVER_IP=`sudo /usr/local/sbin/httpd -d \"$SERVER_IP\"`
LOGLEVEL=`sudo /usr/local/sbin/httpd -d \"$LOGLEVEL\"`
LOGFILE=`sudo /usr/local/sbin/httpd -d \"$LOGFILE\"`
DSDOUT=`sudo /usr/local/sbin/httpd -d \"$DSDOUT\"`
VISULIZER=`sudo /usr/local/sbin/httpd -d \"$VISULIZER\"`
CLOSEOUT=`sudo /usr/local/sbin/httpd -d \"$CLOSEOUT\"`
OTHER=`sudo /usr/local/sbin/httpd -d \"$OTHER\"`

# Save the parameters to the config file
pcp_save_to_config

. $CONFIGCFG

pcp_show_config_cfg
pcp_backup
pcp_go_back_button

echo '</body>'
echo '</html>'