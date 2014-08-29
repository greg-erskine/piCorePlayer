#!/bin/sh
. pcp-functions
pcp_variables

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <meta http-equiv="Refresh" content="5; url=tweaks.cgi">'
echo '  <title>pCP - Change Password</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Change Password" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Decode variables using httpd
NEWPASSWORD=`sudo /usr/local/sbin/httpd -d $NEWPASSWORD`
CONFIRMPASSWORD=`sudo /usr/local/sbin/httpd -d $CONFIRMPASSWORD`

if [ $NEWPASSWORD = $CONFIRMPASSWORD ]; then
	[ $DEBUG = 1 ] && echo '<p class="info">[ INFO ] Passwords OK. '$NEWPASSWORD' = '$CONFIRMPASSWORD'</p>'
	echo '<p class="info">[ INFO ] '
	echo "tc:"$NEWPASSWORD | sudo chpasswd
	echo '</p>'
	pcp_backup
	#####################################
	# TODO. Add code to update httpd.conf
	#####################################
else
	echo '<p class="error">[ ERROR ] Passwords NOT OK. '$NEWPASSWORD' ne '$CONFIRMPASSWORD'</p>'
fi

pcp_go_back_button

echo '</body>'
echo '</html>'
