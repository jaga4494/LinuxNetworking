Write a shell script to do the following tasks:

1. Log the CPU load averages in a CSV file with T second granularity. (format of csv: timestamp, 1 min
load average, 5 min load average, 15 min load average)
2. Generate alert
(a) "HIGH CPU usage" if CPU usage in last one minute is more than a user defined threshold X.
(b) "Very HIGH CPU usage" if CPU usage in last 5 minutes is more than a user defined threshold Y.
Log alert messages in a separate CSV as timestamp, alert String, CPU load Average
3. Clear the log files every hour.
