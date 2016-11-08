#!/usr/bin/python
import sys

def main(argv):
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

if __name__ == "__main__":
    main(sys.argv[1:])
