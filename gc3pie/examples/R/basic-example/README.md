#

Use the following command to run the example:

	python do_multiple_sums.py R.sh sum.R 10 --new -C 5 -r localhost

		do_multiple_sums.py	gc3pie workflow.
		R.sh			A bash script to invoke R.
		sum.R			The R script we want to execute.
		10			Number of replicas.
		--new			Abort previous jobs of the session within session do_multiple_sums.
		-C 5			Make a pause of 5 seconds.
		-r localhost		Use resource localhost.

If all jobs have terminated with success you can dump the results executing the folowing command:

	cat sum.d-*/stdout.txt

The results should be something like this:

	10+34=44
	47+81=128
	84+4=88
	81+67=148
	92+70=162
	28+50=78
	95+81=176
	32+55=87
	87+21=108
	72+35=107
