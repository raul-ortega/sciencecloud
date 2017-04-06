#

Use the following command to run the example:

	python do_multiple_sums.py R.sh sum.R numbers.csv --new -C 5 -r localhost

		do_multiple_sums.py	gc3pie workflow.
		R.sh			A bash script to invoke R.
		sum.R			The R script which will compute each sum.
		numbers.csv		Number of replicas.
		--new			Abort previous jobs of the session within session do_multiple_sums.
		-C 5			Makes a pause of 5 seconds.
		-r localhost		Uses resource localhost.

If all jobs have terminated with success you can dump the results executing the folowing command:

	cat sum.d-*/stdout.txt

The results should be something like this:

	2+2=4
	1+1=2
	3+8=11
	5+2=7
	6+9=15
	30+70=100
	2+98=100
	2+98=100
	40+60=100
	0+88=88
