#! /usr/bin/env python

import os
from os.path import abspath, basename
import sys

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

    Call this python script as:

	    python do-multiple-sums.py bash_file number_of_replicas
	
    The bash script is called as:

	    ./sum.sh

    """
    def __init__(self):
        super(BashScript, self).__init__(version='1.0')
    def setup_args(self):
	# files
	self.add_param('bash',type=existing_file,help="Bash script file to be executed on the remote machine")

	# integers
	self.add_param('number_of_replicas',type=int,help="Total number of replicas")

    def new_tasks(self, extra):
        # Execute tasks in parallel

	# initialize list
        apps_to_run = []
	
	# get full path of the bash script file
	bash_file = abspath(self.params.bash)

	# append tasks to the list
	for index in range(1,self.params.number_of_replicas + 1):
	    apps_to_run.append(BashApp(bash_file, index))
	
	return apps_to_run

class BashApp(Application):
    """Run simulations"""
    def __init__(self, bashscript, index):

	bash_script = basename(bashscript)

        Application.__init__(
            self,
            arguments=["./"+ bash_script],
            inputs=[bashscript],
            outputs=[],
            output_dir = "sum.d-" + `index`,
            stdout="stdout.txt",
            stderr="stderr.txt")



