#! /usr/bin/env python

from subprocess import call # para ejecutar comandos bash

import os
from os.path import abspath, basename
import sys
import csv
from numpy import genfromtxt

from gc3libs import Application
from gc3libs.cmdline import SessionBasedScript, \
	existing_file, positive_int

from gc3libs.quantity import GB


# 1) run python script (sum two numbers)
# 2) Collect results and calculate average.
#
#

# .      .------------------.       .------------------.       .------------------. 
# .      |  run c program   |       |  run c program   | ..... |  run c program   |
# .      `------------------'       `------------------'       `------------------'
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
# .                     .--------------------------------------.
# .                     |  collect data and calculate average  |
# .                     |          - bash script -             |
# .                     `--------------------------------------'


if __name__ == '__main__':
    from do_multiple_sums import ProgramScript
    ProgramScript().run()

class ProgramScript(SessionBasedScript):
    """
    This script calculate n replicas of a sum of 2 numbers.

    Each individual sum is performed by a compiled c program.

    Different pairs of numbers to be sum are provided for the different replicas.

    Call this python script as:

	 python do-multiple-sums.py program_file input_data_file 


    The program sum is called as:

	./sum A B
	
	where A and B are integer numbers.


    """
    def __init__(self):
        super(ProgramScript, self).__init__(version='1.0')
    def setup_args(self):
	# files
	self.add_param('program',type=existing_file,help="Python script file to be executed on the remote machine")
	self.add_param('numbers_to_sum',type=existing_file,help="csv file with input numbers")

    def new_tasks(self, extra):
	session_path = self.session.path.split('/')
	session_name = session_path[len(session_path)-1]

        # Execute tasks in parallel
        apps_to_run = []

	#bash_file = abspath(self.params.bash)
	program_file = abspath(self.params.program)
	numbers_file = abspath(self.params.numbers_to_sum)

	#for index in range(1,self.params.number_of_replicas + 1):
	#    apps_to_run.append(ProgramApp(bash_file, program_file, numbers_file, index))

	with open(numbers_file, 'rb') as f:
	    reader = csv.reader(f)
	    rows = list(reader)

	for row in rows:
	    replicaIndex = row[0]
	    numberA = row[1]
	    numberB = row[2]
	    apps_to_run.append(ProgramApp(program_file, replicaIndex, numberA, numberB))
	
	return apps_to_run

    def after_main_loop(self):
	ntasks = len(self.session.tasks.values())
	session_path = self.session.path.split('/')
	session_name = session_path[len(session_path)-1]

	call(["./collect_data.sh",session_name,`ntasks`,"sum.d-"]) #para ejecutar el script bash


class ProgramApp(Application):
    """Run simulations"""
    #def __init__(self, ProgramScript, program, numbers, index):
    def __init__(self, program, index, A, B):

	#bash_script = basename(ProgramScript)
	sum_program = basename(program)
	
        Application.__init__(
            self,
	    arguments=["./" + sum_program, A,B],
            inputs=[program],
            outputs=[],
            #output_dir = "sum.d-" + `index`,
	    output_dir = "sum.d-" + index,
            stdout="stdout.txt",
            stderr="stderr.txt")



