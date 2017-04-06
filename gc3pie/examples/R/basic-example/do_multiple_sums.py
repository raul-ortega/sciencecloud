#! /usr/bin/env python

import os
from os.path import abspath, basename
import sys

from gc3libs import Application
from gc3libs.cmdline import SessionBasedScript, \
	existing_file, positive_int
	
#
# 1) Copy files
# 2) Run simulations
# 3) Collect data (manually)
#
#

# .      .----------------.       .----------------.         .----------------. 
# .      |  run R script  |       |  run R script  | .....   |  run R script  | 
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
# .                        .-----------------------------------.
# .                        | collect data from standard ouput  |
# .                        `-----------------------------------'


if __name__ == '__main__':
    from do_multiple_sums import RScript
    RScript().run()

class RScript(SessionBasedScript):
    """
    This script executes N replicas of a sum of 2 random numbers.

    Each individual sum is performed by a R script.

    Call this python script as:

	    python do-multiple-sums.py Bash_file R_file number_of_replicas

		Bash_file is used to invoke the R command
	
		R_file is the R script we want to run.
	
    The R script is invoked from the bash script as:

	 /usr/bin/R --slave --vanilla < sum.R 2>/dev/null | sed 's/\[1\] \"//g' | sed 's/\"//g'

	 --slave		Make R run as quietly as possible. This option is intended to support programs which use R to compute 					results for them. It implies --quiet and --no-save. 		
	 --vanilla		Combines --no-save, --no-environ, --no-site-file, --no-init-file and --no-restore.	
	  			https://cran.r-project.org/doc/manuals/R-intro.html#Invoking-R-from-the-command-line

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



