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
    from do_multiple_sums import RScript
    RScript().run()

class RScript(SessionBasedScript):
    """
    This script executes N replicas of a sum of 2 random numbers.

    Each individual sum is performed by a R script.

    Call this python script as:

	    python do-multiple-sums.py R_file number_of_replicas
	
    The R script is called as:

	    R --quiet --vanilla < sum.R  | grep '\[1\]' | sed 's/\[1\] \"//g' | sed 's/\"//g'

    """
    def __init__(self):
        super(RScript, self).__init__(version='1.0')
    def setup_args(self):
	# files
	self.add_param('bash_script',type=existing_file,help="Bash script file to be executed on the remote machine")
	self.add_param('R_script',type=existing_file,help="R script file to be executed on the remote machine")

	# integers
	self.add_param('number_of_replicas',type=int,help="Total number of replicas")

    def new_tasks(self, extra):
        # Execute tasks in parallel

	# initialize list
        apps_to_run = []
	
	# get full path of the R script file
	R_file = abspath(self.params.R_script)
	bash_file = abspath(self.params.bash_script)

	# append tasks to the list
	for index in range(1,self.params.number_of_replicas + 1):
	    apps_to_run.append(RApp(bash_file,R_file, index))
	
	return apps_to_run

class RApp(Application):
    """Run simulations"""
    #arguments=["R --quiet --vanilla --slave < ./" + R_script + " 2>/dev/null | sed 's/\[1\] \"//g' | sed 's/\"//g'"],
    def __init__(self,BashScript, RScript, index):
	
	bash_script = basename(BashScript)
	R_script = basename(RScript)

        Application.__init__(
            self,
	    arguments=["./" + bash_script],
            inputs=[BashScript,RScript],
            outputs=[],
            output_dir = "sum.d-" + `index`,
            stdout="stdout.txt",
            stderr="stderr.txt")



