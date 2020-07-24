#!/usr/bin/python

import sys
import getopt
import math
import argparse
import os
import print_util
import util
from cache import Cache
from slice import Slice

#python3 Mile1.py -f Trace1.trc -s 512 -b 16 -a 8 -r Random

#print ('Number of arguments:', len(sys.argv))
#print ('Argument List:', str(sys.argv[1:]))

def get_row_set_from_cache(access_list):
    cache_offset = cache.get_offset()
    cache_index_size = cache.get_index_size()
    for entry in access_list:
        split = entry.split(',')
        sliced_address = Slice(split[0], cache_offset, cache_index_size)
        cache_row_set = cache.read_cache(int(split[1]), util.bin_to_dec(sliced_address.get_offset()),
                                         sliced_address.get_index())
        access_the_cache(cache_row_set, util.bin_to_hex(sliced_address.get_tag()))


def access_the_cache(cache_rows, tag):
    global cache_accesses
    cache_accesses += len(cache_rows)

    for row in cache_rows:
        check_cache(row, tag)


def check_cache(row, tag):
    global compulsory_misses
    global cache_hits
    global conflict_misses
    global cycle_total
    for i in range(len(row)):
        block = row[i]
        if block.valid == 0:
            compulsory_misses += 1
            block.tag = tag
            block.valid = 1
            cycle_total += (4*math.ceil(blockSize/4))
            break
        else:
            if i == len(row) - 1 and block.tag != tag:
                conflict_misses += 1
                # Random Replace
                if args.replacement == 'RND':
                    random_num = util.calculate_random_number(0, (len(row) - 1))
                    row[random_num].tag = tag
                    break
                # - Robin
                if args.replacement == 'RR':
                    round_robin_index = util.determine_round_robin(row)
                    row[round_robin_index].tag = tag
                    break
            elif block.tag == tag:
                cache_hits += 1
                cycle_total += 1
                break
            else:
                continue

# User input control
parser = argparse.ArgumentParser(description='Pull user args for sim cache')
parser.add_argument('-f', '--trace', type=str , metavar='', required=True, help='name of text file with the trace')
parser.add_argument('-s', '--cachesize', type=int, metavar='', required=True, help='1 KB to 8 MB')
parser.add_argument('-b', '--blocksize', type=int, metavar='', required=True, help='4 bytes to 64 bytes')
parser.add_argument('-a', '--associativity', type=int, metavar='', required=True, help='1, 2, 4, 8, 16')
parser.add_argument('-r', '--replacement', type=str, metavar='', required=True, help='RR or RND', choices=['RR', 'RND'])
args = parser.parse_args()

# Global values
cache_accesses = 0
cache_hits = 0
compulsory_misses = 0
conflict_misses = 0
cycle_total = 0
intruction_count = 0
#regex = re.compile("EIP\s\(([0-9]{2})\):\s([^\s]+)")
#argv = str(sys.argv[1:])
traceFile = args.trace
cacheSize = args.cachesize
blockSize = args.blocksize
mapWay = args.associativity
repPolicy = args.replacement

print("Trace is", traceFile, " Cache size is", cacheSize, " Blocksize is ", blockSize, " Associativity is ", mapWay, "Replacement alg is ", repPolicy)
#print ('opts is:', opts)
#print ('opt is ', opt, 'arg is ', arg)
#args.cachesize, args.blocksize, args.associativity, args.replacement


##print ('Cache Simulator CS 3853 Summer 2020 - Group#05')
##print ('')
##print ('Trace File:', traceFile)
##print ('')
##print ('***** Cache Input Parameters *****')
##print ('Cache size:', cacheSize, 'KB')
##print ('Block size:', blockSize, 'bytes')
##print ('Associativity:', mapWay)
##print ('Replacement policy:', repPolicy)
##print ('')
##print ('***** Cache Calculated Values *****')
##print ('')

totalBlock = int((math.pow(2, math.log2(int(cacheSize)))*(math.pow(2,10)))/int(blockSize))
indexSize = int(int(math.log2(int(cacheSize)) + int(10)) - math.log2(int(blockSize)*int(mapWay)))
tagSize = int(int(32) - math.log2(int(blockSize)) - indexSize)
totalRows =  int(math.pow(2, int(int(math.log2(int(cacheSize)) + int(10)) - math.log2(int(blockSize)*int(mapWay)))))
overheadSize = int(((tagSize+1)*totalBlock)/int(mapWay))
impMemByteSize = int((math.pow(2, math.log2(int(cacheSize)))*(math.pow(2,10))) + overheadSize)
impMemKBSize = math.pow(2,(math.log2(impMemByteSize)-10))

#print ('Total # of Blocks:', totalBlock)
#print ('Tag Size:', tagSize, 'bits')
#print ('Index Size:', indexSize, 'bits')
#print ('Total # Rows:', totalRows)
#print ('Overhead Size:', overheadSize, 'bytes')
#print ('Implemention Memory Size:', "{:.2f}".format(impMemKBSize), 'KB (' + str(impMemByteSize), 'Bytes)')
#print ('Cost: $', "{:.2f}".format(0.07*impMemKBSize))
#print ('')
## Output data
#f = open(traceFile, 'r')
#lines = f.read()
#match = re.findall('EIP\s\(([0-9]{2})\):\s([^\s]+)', lines)
#
#for i in range(20):
#    print('0x' + match[i][1] + ':' + match[i][0])
#f.close()
#print ('Initialize the timer and counter...Done')
#
#print ('Call the space for Cache Simulator...Done')

tupl = util.parse_file(traceFile)
cache_access_list = tupl[0]
intruction_count = tupl[1]

# Create the cache access list
cache = Cache(cacheSize, blockSize, mapWay, repPolicy)

# Iterate through accesses
get_row_set_from_cache(cache_access_list)

# Print the specified results
print_util.print_formatted_header(traceFile)
print_util.print_generic_header(cacheSize, blockSize, mapWay, repPolicy) # ***** Cache Input Parameters *****
print_util.print_calculated_values(cache.get_num_blocks(), cache.get_tag_size(), cache.get_indices(),
                                   cache.get_index_size(), cache.get_overhead_size(), cache.get_total_size())
print_util.print_results(cache_accesses, cache_hits, conflict_misses, compulsory_misses, totalBlock, blockSize, overheadSize, impMemKBSize, cache.get_total_size(), cycle_total, intruction_count) # ***** Cache Simulation Results *****
