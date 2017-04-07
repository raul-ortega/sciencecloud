#! /usr/bin/env python

import os
from os.path import abspath, basename
import sys

from random import randint

from gc3libs import Application
from gc3libs.cmdline import SessionBasedScript, \
	existing_file, positive_int
	
#
# 1) Copy files
# 2) Run simulations
# 3) Collect data
#
#

# .      .------------------.     .------------------.       .------------------.
# .      |run python script |     |run python script | ..... |run python script | 
# .      `------------------'     `------------------'       `------------------' 
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
    from do_multiple_sums import PythonScript
    PythonScript().run()

class PythonScript(SessionBasedScript):
    """
    This script calculate n replicas of a sum of 2 numbers randomly generated.

    Each individual sum is performed by a python script.

    Call this python script as:

	    python do-multiple-sums.py program_file number_of_replicas
	
    The python sum.py script is called as:

	    /usr/bin/python sum.py A B

    where A and B are integer numbers.

    """
    def __init__(self):
        super(PythonScript, self).__init__(version='1.0')
    def setup_args(self):
	# files
	self.add_param('program',type=existing_file,help="Python script to be executed on the remote machine")
	# integers
	self.add_param('number_of_replicas',type=int,help="Total number of replicas")

    def new_tasks(self, extra):
        # Execute tasks in parallel

        apps_to_run = []

	program_file = abspath(self.params.program)

	for index in range(1,self.params.number_of_replicas + 1):
	    A = randint(1, 100)
	    B = randint(1, 100)
	    apps_to_run.append(PythonApp(program_file, index, A, B))
	
	return apps_to_run

class PythonApp(Application):
    """Run simulations"""
    def __init__(self, python_file, index, numberA, numberB):

	python_script = basename(python_file)

        Application.__init__(
            self,
            arguments=["/usr/bin/python", python_script, numberA, numberB],
            inputs=[python_file],
            outputs=[],
            output_dir = "sum.d-" + `index`,
            stdout="stdout.txt",
            stderr="stderr.txt")



