import argparse
import os
import sys
import re
from random import randint


def determine_valid_file(string):
    if os.path.isfile(string):
        return string
    else:
        raise argparse.ArgumentTypeError('file ' + string + ' does not exist')


def cache_size_type(string, min_param=1, max_param=8192):
    value = int(string)
    if min_param <= value <= max_param:
        return value
    else:
        raise argparse.ArgumentTypeError('value not in range ' + str(min_param) + ' - ' + str(max_param))


def block_size_type(string, min_param=4, max_param=64):
    value = int(string)
    if min_param <= value <= max_param:
        return value
    else:
        raise argparse.ArgumentTypeError('value not in range ' + str(min_param) + ' - ' + str(max_param))


def calculate_random_number(min_param, max_param):
    return randint(min_param, max_param)


def hex_to_bin(hex_value):
    return bin(int(hex_value, 16))[2:].zfill(32)


def bin_to_hex(bin_value):
    return hex(int(bin_value, 2))


def bin_to_dec(bin_value):
    return int(bin_value, 2)


def parse_file(file):
    empty = '0x00000000'
    cache_access_list = []
    intruction_count = 0
    try:
        with open(file, 'r') as f:
            for line in f:
                info = re.match(r'^.+\((\d{2})\).\s(.{8}).+$', line)
                read_write = re.match(r'^.+:\s(\w{8}).*:\s(\w{8}).*$', line)
                if info:
                    intruction_count += 1
                    address = '0x' + info.group(2)
                    length = int(info.group(1))
                    cache_access_list.append(address + ',' + str(length))
                if read_write:
                    write_address = '0x' + str(read_write.group(1))
                    read_address = '0x' + str(read_write.group(2))
                    if write_address != empty:
                        cache_access_list.append(write_address + ',4')
                    if read_address != empty:
                        cache_access_list.append(read_address + ',4')
    except FileNotFoundError:
        print('Error: File was not found')
        print('Please check that the file exists and try again')
        sys.exit(2)
    return cache_access_list, intruction_count


def determine_round_robin(current_row):
    for i in range(len(current_row)):
        if current_row[i].used == 0:
            current_row[i].used = 1
            return i
        elif current_row[i].used == 1 and len(current_row) == i + 1:
            for j in range(len(current_row)):
                current_row[j].used = 0
            return 0
