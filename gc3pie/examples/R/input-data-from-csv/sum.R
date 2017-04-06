# Launch from command line as:
args = commandArgs(trailingOnly=TRUE)

if (length(args)==2) {
  # Get args
  A = as.integer(args[1])
  B = as.integer(args[2])
  C = A + B
  # Sum the numbers and echo the result to stdout
  print(paste(A,"+",B,"=",C,sep=""))
} else {
  stop("At least three argument must be supplied (input file).n", call.=FALSE)  
}


