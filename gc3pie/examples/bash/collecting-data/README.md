#

Use the following command to run the example:

	python do_multiple_sums.py sum numbers.csv -C 2 --new -r localhos

		do_multiple_sums.py	gc3pie workflow.
		sum			A compiled C program (source code in sum.c)
		numbers.csv		Number of replicas.
		--new			Abort previous jobs of the session within session do_multiple_sums and send new jobs.
		-C 5			Makes a pause of 5 seconds.
		-r localhost		Uses resource localhost.

If all jobs have terminated with success, after statistics will be shown the messages:

	All jobs have finished with success

	The average sum is: 19.20


You can dump the results of the sums executing the folowing command:

	find sum.d-* -type f -name "stdout.txt" | grep "[0-9]/" | xargs cat

The results should be something like this:

	1+1=2
	3+8=11
	4+5=9
	50+20=70
	2+2=4
