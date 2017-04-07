import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
args = parser.parse_args()
a = args.integers[0]
b = args.integers[1]
c = sum(parser.parse_args().integers)
print("%r+%r=%r" % (a,b,c))
