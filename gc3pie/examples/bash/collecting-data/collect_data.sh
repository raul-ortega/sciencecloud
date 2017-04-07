#!/bin/bash

# arguments
session_name=$1 # Name of the session
session_tasks=$2 # Number of tasks of the session
tasks_outdir_prefix=$3 # Prefix of the path where each task stores its output files

# Get the number of taks which have finished with success
successful_tasks=$(gselect --successful -s do_multiple_sums 2>/dev/null | wc -l)

# Check how many tasks have finished with success
if [[ $successful_tasks -eq $session_tasks ]];then

	echo;echo "All jobs have finished with success"

	# write your code to collect data here
 	# For example we are going to calculate the average sum
	
	tasks_indexes=$(seq 1 $successful_tasks)
	acc_sum=0

	# For each task
	for i in $tasks_indexes
	do
		# get its output directory
		task_path=$tasks_outdir_prefix$i 

		# get the result of the sum from the stdout.txt file
		sum=$(cat $task_path/stdout.txt | awk -F'=' '{print $2}')
		
		# add sum to the accumulated sum
		let acc_sum=acc_sum+$sum
	done
	
	# Calculate average
	average_sum=$(echo "scale=2;$acc_sum/$successful_tasks" | bc)
	
	# Print the result
	echo;echo "The average sum is: $average_sum"
elif [[ $tasksOk -lt $sessionTasks ]];then
	echo;echo "Only $tasksOk of $sessionTasks tasks have finished with success"

	# Here you could use the gc3pie tool "gcloud list" together with "grep" and "awk"
	# to extratc the IP address of the virtual machines which haven't fihished yet
	# and get some info from them using ssh
else
	echo;echo "No tasks have finished with success"

	# Here you could use the gc3pie tool "gcloud list" together with "grep" and "awk"
	# to extratc the IP address of the virtual machines which haven't fihished yet
	# and get some info from them using ssh
fi
echo
