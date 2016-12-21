#!/bin/bash

# Generate two random numbers between 1 and 100
A=$(((RANDOM % 100) + 1))
B=$(((RANDOM % 100) + 1))

# Sum the numbers and echo the result to stdout
echo "$A+$B="$(($A+$B))

