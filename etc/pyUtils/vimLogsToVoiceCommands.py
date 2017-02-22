import sys

logfile = open(sys.argv[1], 'r')
print sys.argv[1]
print logfile.readline()
