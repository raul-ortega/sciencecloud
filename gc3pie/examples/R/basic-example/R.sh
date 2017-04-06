#!/bin/bash

/usr/bin/R --slave --vanilla < sum.R 2>/dev/null | sed 's/\[1\] \"//g' | sed 's/\"//g'

# --slave		Make R run as quietly as possible. This option is intended to support programs which use R to compute results 				for them. It implies --quiet and --no-save. 		
# --vanilla		Combines --no-save, --no-environ, --no-site-file, --no-init-file and --no-restore.	
# 			https://cran.r-project.org/doc/manuals/R-intro.html#Invoking-R-from-the-command-line

# 2>/dev/null		Suppress "During startup - Warning messages"
# sed 's/\[1\] \"//g'	To remove [1]
# sed 's/\"//g'		To remove "

