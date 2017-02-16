#!/bin/bash
# 
# This tool will provide the ip of the host which execuited each task
#
# Execution:
# 	./get_hosts_ip.sh mysession
#
# $1: gets the name of the session
#

gcloud list 2> /dev/null > hosts.txt

jobs=$(ls $1/jobs)
for job in $jobs
do
	ip=""
	id=""

	id=$(ginfo -s $1 $job -v 2> /dev/null | grep "_lrms_vm_id: " | awk -F' ' '{print $2}')
	if [ "$id" = "" ];then
		echo -e $job "\tvms not found"
	else
		ip=$(grep "$id" hosts.txt | sed 's/ | /,/g' | awk -F',' '{print $4}')
		echo -e $job"\t"b$id"\t"$ip
	fi
done
