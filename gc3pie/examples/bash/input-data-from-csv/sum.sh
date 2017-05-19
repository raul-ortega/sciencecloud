#!/bin/bash

# Read the line which start with index number $1
line=$(grep "^$1," ./numbers.csv)

# get the numbers to be summed
A=$(echo $line | awk -F',' '{print $2}')
B=$(echo $line | awk -F',' '{print $3}')

# Sum the numbers and echo the result to stdout
echo "$A+$B="$(($A+$B))
