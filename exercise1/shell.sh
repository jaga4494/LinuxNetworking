#!/bin/bash
# CSV file to log CPU load averages
loadfile=load.csv
# CSV file to log CPU usage alert
alertfile=alert.csv
# Set T=10 seconds as granularity [interval between each load capture]
T=10
# Time since the log is created. When it reaches 3600, log files are cleared
logTime=0
# Clear the log every one hour
logClearTime=3600
# Threshold for last 1 minute load average
X=0.1
# Threshold for last 5 minutes load average
Y=0.2
# Alert message for 1 minute usage
highcpu="HIGH CPU usage"
# Alert message for 5 minutes usage
veryhighcpu="Very HIGH CPU usage"
while :
do
	# Command to extract timestamp and load averages for 1,5,15 minute
	output="$(uptime | grep -ohe '.* up .*' | awk '{ print $1","$10$11$12 }')"
	echo $output
	# log the entry in loadfile
	echo "$output" >> "$loadfile"
	# Extract the timestamp
	timestamp=`echo $output | grep -ohe '.*[,].*' | awk -F, '{print $1}'`
	# Extract the oneminute load average
	oneminute=`echo $output | grep -ohe '.*[,].*' | awk -F, '{print $2}'`
	# Extract the fiveminute load average
	fiveminute=`echo $output | grep -ohe '.*[,].*' | awk -F, '{print $3}'`
	# Check whether oneminute load average is more than threshold, X
	if [ `echo "$oneminute > $X" | bc` -eq 1 ];	then
		# Generate oneminute load average alert
		echo -e "\nAlert: $highcpu"
		# Log the entry in alertfile
		echo "$timestamp","$highcpu","$oneminute" >> "$alertfile"
	fi
	# Check whether fiveminute load average is more than threshold, Y
	if [ `echo "$fiveminute > $Y" | bc` -eq 1 ];	then
		# Generate fiveminute load average alert
		echo -e "\nAlert: $veryhighcpu"
		# Log the entry in alertfile
		echo "$timestamp","$veryhighcpu","$fiveminute" >> "$alertfile"
	fi
	# Sleep for T seconds
	sleep $T
	# Calculate the time since log file is last cleared or created
	logTime=$((logTime+T))
	# If log files is created before or cleared before 1 hour, they are cleared again
	if [ `echo "$logTime >= $logClearTime" | bc` -eq 1 ];	then
		echo -n "" > "$loadfile"
		echo -n "" > "$alertfile"
		# log creation time is again set to 0
		logTime=0
		echo -e "\nlog files cleared"
	fi
	echo -e "\n-----------------------------------------"
done
