jobs=$(ls $1/jobs)
for job in $jobs
do
	ip=""
	id=""

	id=$(ginfo -s $1 $job -v 2> /dev/null | grep "_lrms_vm_id: " | awk -F' ' '{print $2}')
	if [ "$id" = "" ];then
		echo -e $job "\tvms not found"
	else
		ip=$(gcloud list 2> /dev/null | grep "$id" | sed 's/ | /,/g' | awk -F',' '{print $4}')
		echo -e $job"\t"b$id"\t"$ip
	fi
done
