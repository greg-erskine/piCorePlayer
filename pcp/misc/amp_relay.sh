#!/bin/sh

# Version: 0.01 2014-11-28 GE
#	Original.

#===========================================================================
# This script polls LMS at a regular interval to determine the current
# status of the Squeezelite process on piCorePlayer. i.e. play or stop.
#
# A GPIO is then set/reset depending on the result of this status check.
#
# There is an adjustable relay off delay that can be used as an inactivity
# timing.
#---------------------------------------------------------------------------

#===========================================================================
# Possible issues
#---------------------------------------------------------------------------
# 1. Initial relay status during booting. It is probably better to start
#    this script before starting Squeezelite. Also, a pull-up or pull-down
#    resistor may be needed to ensure initial state of GPIO.
# 2. If setting MAC address manually, pay close attention to the physical,
#    wireless and fake MAC addresses.
# 3. This script hasn't been tested on synced players.
#---------------------------------------------------------------------------

#===========================================================================
# Test procedure
#---------------------------------------------------------------------------
# sudo killall relay.sh
# sudo sh -c 'echo "17" > /sys/class/gpio/unexport'
# sudo ./relay.sh > /dev/null &
#---------------------------------------------------------------------------

set -x
#. /home/tc/www/cgi-bin/pcp-functions
#pcp_variables

#===========================================================================
# Set the following according to your setup
#---------------------------------------------------------------------------
MAC_ADDR=b8%3A27%3Aeb%3Ac7%3Ae0%3A61		# Raspberry Pi MAC address
#MAC_ADDR=$(pcp_controls_mac_address)		# Set by pCP
LMS_IP=192.168.1.101						# LMS IP address
#LMS_IP=$(pcp_lmsip)						# Set by pCP
INTERVAL=0.5								# Set Poll interval
GPIO=17										# Set GPIO
COMMAND="status 0 0"						# LMS player status command
DELAYOFF=10									# Delay in no. of intervals
COUNT=0
DEBUG=1
#---------------------------------------------------------------------------

if [ $DEBUG = 1 ]; then
	echo
	echo "MAC_ADDR : "$MAC_ADDR
	echo "LMS_IP   : "$LMS_IP
	echo "INTERVAL : "$INTERVAL
	echo "GPIO     : "$GPIO
	echo "COMMAND  : "$COMMAND
	echo "DELAYOFF : "$DELAYOFF
	echo
fi

get_mode() {
	RESULT=`( echo "$MAC_ADDR $COMMAND"; echo exit ) | nc $LMS_IP 9090`
	echo $RESULT | grep "mode%3Aplay" > /dev/null 2>&1
	if [ $? == 0 ]; then
		echo "Playing. Count: $COUNT"
		COUNT=0
		echo "1" > /sys/class/gpio/gpio$GPIO/value
	else
		if [ $COUNT -ge $DELAYOFF ]; then
			#echo "Stopped. Count: $COUNT"
			echo "0" > /sys/class/gpio/gpio$GPIO/value
			COUNT=0
		else
			#COUNT=`expr $COUNT + 1` #or
			COUNT=$(($COUNT + 1))
			echo "Stopped. Count: $COUNT"
		fi
	fi
}

#===========================================================================
# Initial GPIO setup
#---------------------------------------------------------------------------
sudo sh -c 'echo '"$GPIO"' > /sys/class/gpio/export'
sudo sh -c 'echo "out" > /sys/class/gpio/gpio'"$GPIO"'/direction'
# My relay is active low, so this reverses the logic
sudo sh -c 'echo "1" > /sys/class/gpio/gpio'"$GPIO"'/active_low'
echo "0" > /sys/class/gpio/gpio$GPIO/value
#---------------------------------------------------------------------------

#===========================================================================
# Loop forever. This uses less the 1% CPU, so it should be OK.
#---------------------------------------------------------------------------
while true
do
	get_mode
	sleep $INTERVAL
done
#--------------------------------------------------------------------------- 
