#!/usr/bin/python

import sys
import getopt
import math
import argparse

#python3 Mile1.py -f Trace1.trc -s 512 -b 16 -a 8 -r Random

#print ('Number of arguments:', len(sys.argv))
#print ('Argument List:', str(sys.argv[1:]))

# User input control
parser = argparse.ArgumentParser(description='Pull user args for sim cache')
parser.add_argument('-f', '--trace', type=str , metavar='', required=True, help='name of text file with the trace')
parser.add_argument('-s', '--cachesize', type=int, metavar='', required=True, help='1 KB to 8 MB')
parser.add_argument('-b', '--blocksize', type=int, metavar='', required=True, help='4 bytes to 64 bytes')
parser.add_argument('-a', '--associativity', type=int, metavar='', required=True, help='1, 2, 4, 8, 16')
parser.add_argument('-r', '--replacement', type=str, metavar='', required=True, help='RR or RND or LRU')
args = parser.parse_args()

traceFile = ''
cacheSize = ''
blockSize = ''
mapWay = ''
repPolicy = ''
#argv = str(sys.argv[1:])

def main(trace, cachesize, blocksize, associativity, replacement):
    print("Trace is", trace, " Cache size is", cachesize, " Blocksize is ", blocksize, " Associativity is ", associativity, "Replacement alg is ", replacement)
    #print ('opts is:', opts)
    #print ('opt is ', opt, 'arg is ', arg)
    traceFile = trace
    cacheSize = cachesize
    blockSize = blocksize
    mapWay = associativity
    repPolicy = replacement

    print ('Cache Simulator CS 3853 Summer 2020 - Group#05')
    print ('')
    print ('Trace File:', traceFile)
    print ('')
    print ('***** Cache Input Parameters *****')
    print ('Cache size:', cacheSize, 'KB')
    print ('Block size:', blockSize, 'bytes')
    print ('Associativity:', mapWay)
    print ('Replacement policy:', repPolicy)
    print ('')
    print ('***** Cache Calculated Values *****')
    print ('')

    totalBlock = int((math.pow(2, math.log2(int(cacheSize)))*(math.pow(2,10)))/int(blockSize))
    indexSize = int(int(math.log2(int(cacheSize)) + int(10)) - math.log2(int(blockSize)*int(mapWay)))
    tagSize = int(int(32) - math.log2(int(blockSize)) - indexSize)
    totalRows =  int(math.pow(2, int(int(math.log2(int(cacheSize)) + int(10)) - math.log2(int(blockSize)*int(mapWay)))))
    overheadSize = int(((tagSize+1)*totalBlock)/int(mapWay))
    impMemByteSize = int((math.pow(2, math.log2(int(cacheSize)))*(math.pow(2,10))) + overheadSize)
    impMemKBSize = math.pow(2,(math.log2(impMemByteSize)-10))

    print ('Total # of Blocks:', totalBlock)
    print ('Tag Size:', tagSize, 'bits')
    print ('Index Size:', indexSize, 'bits')
    print ('Total # Rows:', totalRows)
    print ('Overhead Size:', overheadSize, 'bytes')
    print ('Implemention Memory Size:', "{:.2f}".format(impMemKBSize), 'KB (' + str(impMemByteSize), 'Bytes)')
    print ('Cost: $', "{:.2f}".format(0.07*impMemKBSize))

if __name__ == '__main__':
    main(args.trace, args.cachesize, args.blocksize, args.associativity, args.replacement)
