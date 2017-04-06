#! /usr/bin/env python

import os
from os.path import abspath, basename
import sys
import csv

from gc3libs import Application
from gc3libs.cmdline import SessionBasedScript, \
	existing_file, positive_int
	
#
# 1) Copy input files
# 2) Run simulations
# 3) Collect data 
#
#

# .      .----------------.       .----------------.         .----------------. 
# .      | run R  script  |       | run R  script  | .....   | run R  script  | 
# .      `----------------'       `----------------'         `----------------' 
# .               \                       |                         /
# .                \                      |                        /
# .                 \                     |                       /
# .                  \                    |                      /
# .                   \                   |                     /
# .                    \                  |                    /
# .                     \                 |                   /
# .                      \                |                  /
# .                       \               |                 /
# .                        \              |                /
# .                        .--------------------------------.
# .                        |  collect csv files from ouput  |
# .                        `--------------------------------'


if __name__ == '__main__':
    from do_multiple_sums import RScript
    RScript().run()

class RScript(SessionBasedScript):
    """
    This script executes several sums of pairs of numbers provided through a csv file as input.

    Each individual sum is performed by a R script.

    Call this python script as:

	    python do-multiple-sums.py Bash_file R_file numbers_to_sum

		Bash_file is used to invoke the R command
	
		R_file is the R script we want to run.

		numbers_to_sum is the csv file which contains the pairs of numbers
	
    The R script is invoked from the bash script as:

	 /usr/bin/R --slave --vanilla --args $1 $2 < sum.R 2>/dev/null | sed 's/\[1\] \"//g' | sed 's/\"//g'

	 --slave		Make R run as quietly as possible. This option is intended to support programs which use R to compute 					results for them. It implies --quiet and --no-save. 		
	 --vanilla		Combines --no-save, --no-environ, --no-site-file, --no-init-file and --no-restore.	
	  			https://cran.r-project.org/doc/manuals/R-intro.html#Invoking-R-from-the-command-line

	 --args $1 $2		$1 and $2 are the bash arguments with the numbers to be summed.

	 2>/dev/null		Suppress "During startup - Warning messages"
	 sed 's/\[1\] \"//g'	To remove "[1]"
	 sed 's/\"//g'		To remove quotes

    """
    def __init__(self):
        super(RScript, self).__init__(version='1.0')
    def setup_args(self):
	# files
	self.add_param('bash_script',type=existing_file,help="Bash script file to be executed on the remote machine")
	self.add_param('R_script',type=existing_file,help="R script file to be executed on the remote machine")
	self.add_param('numbers_to_sum',type=existing_file,help="csv file with input numbers")

    def new_tasks(self, extra):
        # Execute tasks in parallel

	# initialize list
        apps_to_run = []
	
	# get full path of the files
	bash_file = abspath(self.params.bash_script)
	R_file = abspath(self.params.R_script)
	numbers_file = abspath(self.params.numbers_to_sum)

	# Read index and pairs of numbers from csv file

	with open(numbers_file, 'rb') as f:
	    reader = csv.reader(f)
	    rows = list(reader)

	replica_index = 0
	for row in rows:
	    replicaIndex = row[0]
	    numberA = row[1]
	    numberB = row[2]
	    #print("index: %r A: %r B: %r\n" % (replicaIndex,numberA,numberB))

	    # Add job to list
	    apps_to_run.append(RApp(bash_file, R_file, replicaIndex, numberA, numberB))
	
	return apps_to_run

class RApp(Application):
    """Run simulations"""
    def __init__(self, bash_file, R_file, index, A, B):
	# Bash script file name
	bash_script = basename(bash_file)

	# R script file name
	R_script = basename(R_file)

	# Submit job
        Application.__init__(
            self,
            arguments=["./" + bash_script, A, B],
            inputs=[bash_file,R_file],
            outputs=[],
            output_dir = "sum.d-" + index,
            stdout="stdout.txt",
            stderr="stderr.txt")



