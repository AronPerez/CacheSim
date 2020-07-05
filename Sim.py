#!/usr/bin/env python3

import sys,math,argparse

#Sim.py
#–f trace1.trc
#–s 512
#–b 16
#–a 2
#–r RR
#print("Usage: python3 Sim.py \n-f trace file name> \n-s <cache size in KB> \n–b <block size> \n–a <associativity> \n–r <replacement policy> ")

parser = argparse.ArgumentParses(description='Pull user args for sim cache')
parses.add_argument('-f', 'trace', type=string, metavar='', required=True, help='name of text file with the trace')
parses.add_argument('-s', 'cachesize', type=int, metavar='', required=True, help='1 KB to 8 MB')
parses.add_argument('-b', 'blocksize', type=int, metavar='', required=True, help='4 bytes to 64 bytes')
parses.add_argument('-a', 'associativity', type=int, metavar='', required=True, help='1, 2, 4, 8, 16')
parses.add_argument('-r', 'replacement', type=string, metavar='', required=True, help='RR or RND or LRU')
args = parser.parse_args()


def main(trace, cachesize, blocksize, associativity, replacement):
    print("Trace is", trace, " Cache size is", cachesize, " Blocksize is ", blocksize, " Associativity is ", associativity, "Replacement alg is ", replacement)

if __name__ = '__main__':
    main(args.trace, args.cachesize, args.blocksize, args.associativity, args.replacement)
