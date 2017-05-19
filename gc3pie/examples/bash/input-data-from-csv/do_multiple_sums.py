#! /usr/bin/env python

import os
from os.path import abspath, basename
import sys
import csv

from gc3libs import Application
from gc3libs.cmdline import SessionBasedScript, \
	existing_file, positive_int
	
#
# 1) Decompress tar file
# 2) Run simulations
# 3) Collect data (manually)
#
#

# .      .----------------.       .----------------.         .----------------. 
# .      |run bash script |       |run bash script | .....   |run bash script | 
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
    from do_multiple_sums import BashScript
    BashScript().run()

class BashScript(SessionBasedScript):
    """
    This script executes N replicas of a sum of 2 random numbers.

    Each individual sum is performed by a bash script.

    Different pairs of numbers to be summed are provided by a common csv file

    Call this python script as:

	    python do-multiple-sums.py bash_file program_file input_data_file
	
    The bash script is called as:

	    ./sum.sh replica_number

    """
    def __init__(self):
        super(BashScript, self).__init__(version='1.0')
    def setup_args(self):
	# files
	self.add_param('bash',type=existing_file,help="Bash script file to be executed on the remote machine")
	self.add_param('numbers_to_sum',type=existing_file,help="csv file with input numbers")

    def new_tasks(self, extra):
        # Execute tasks in parallel

	# initialize list
        apps_to_run = []
	
	# get full path of the files
	bash_file = abspath(self.params.bash)
	numbers_file = abspath(self.params.numbers_to_sum)

	#for index in range(1,self.params.number_of_replicas + 1):
	#    apps_to_run.append(BashApp(bash_file, program_file, numbers_file, index))

	with open(numbers_file, 'rb') as f:
	    reader = csv.reader(f)
	    rows = list(reader)
	replica_index = 0
	for row in rows:
	    replica_index += 1
	    apps_to_run.append(BashApp(bash_file, replica_index))
	
	return apps_to_run

class BashApp(Application):
    """Run simulations"""
    #def __init__(self, bashscript, program, numbers, index):
    def __init__(self, program, index, A, B):

	#bash_script = basename(bashscript)
	sum_program = basename(program)

        Application.__init__(
            self,
            #arguments=["./"+ bash_script, index],
	    arguments=["./"+ sum_program, A,B],
            inputs=[program],
            outputs=[],
            #output_dir = "sum.d-" + `index`,
            output_dir = "sum.d-" + index,
            stdout="stdout.txt",
            stderr="stderr.txt")



