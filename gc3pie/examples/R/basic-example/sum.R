# Launch from command line as:
#	/usr/bin/R --slave --vanilla < sum.R 2>/dev/null | sed 's/\[1\] \"//g' | sed 's/\"//g'

# Generate two random numbers between 1 and 100
A=floor(runif(1,min=1,max=100))
B=floor(runif(1,min=1,max=100))

# Sum the numbers and echo the result to stdout
print(paste(A,"+",B,"=",A+B,sep=""))
