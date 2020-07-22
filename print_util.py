def print_formatted_header(trace_file):
    print ('Cache Simulator CS 3853 Summer 2020 - Group#05')
    print ()
    print ('Trace File: ' + trace_file)
    print ()


def print_generic_header(cache_size, block_size, associativity, replacement_policy):
    print ('***** Cache Input Parameters *****')
    print ()
    print ('{:32}'.format('Cache Size:') + str(cache_size) + ' KB')
    print ('{:32}'.format('Block Size:') + str(block_size) + ' bytes')
    print ('{:32}'.format('Associativity:') + str(associativity))
    print ('{:32}'.format('Replacement Policy:') + replacement_policy)
    print ()


def print_calculated_values(num_blocks, tag_size, indices, index_size, overhead, total_size):
    print ('***** Cache Calculated Parameters *****')
    print ()
    print ('{:32}'.format('Total #Blocks:') + str(num_blocks))
    print ('{:32}'.format('Tag Size:') + str(tag_size) + ' bits')
    print ('{:32}'.format('Index Size:') + str(index_size) + ' bits')
    print ('{:32}'.format('Total # Rows:') + str(indices))
    #overhead_size = overhead/1024
    #overhead_string = '%.2f' % overhead_size
    print ('{:32}'.format('Overhead Memory Size:') + str(overhead) + ' bytes')
    implementation_size = total_size/1024
    implementation_string = '%.2f' % implementation_size
    print ('{:32}'.format('Implementation Memory Size:') + implementation_string + ' KB (' + str(total_size), 'Bytes)')
    print ('Cost: $', "{:.2f}".format(0.07*implementation_size))
    print ()
    print ()


def print_results(cache_accesses, cache_hits, conflict_misses, compulsory_misses, num_blocks, block_size, overhead, associativity, total_size, cycle_total, intruction_count):
    print ('***** Cache Simulation Results *****')
    print ()
    print ('{:24}'.format('Total Cache Accesses:') + str(cache_accesses))
    print ('{:24}'.format('Cache Hits:') + str(cache_hits))
    print ('{:24}'.format('Cache Misses:') + str(conflict_misses + compulsory_misses))
    print ('{:27}'.format('--- Compulsory Misses:') + str(compulsory_misses))
    print ('{:27}'.format('--- Conflict Misses:') + str(conflict_misses))
    print ()
    print ()
    print ('***** ***** CACHE MISS/HIT RATE: ***** *****')
    miss_rate = (conflict_misses + compulsory_misses)/cache_accesses * 100
    hit_rate = 100 - miss_rate
    miss_rate_string = 'Cache Miss Rate: %.4f' % miss_rate
    hit_rate_string = 'Cache Hit Rate: %.4f' % hit_rate
    Unused_KB = (((num_blocks)-(compulsory_misses)) * ((block_size*.001)+(overhead*.001)))/(associativity*block_size)
    Unused_string = '%.2f' % Unused_KB
    implementation_size = total_size/1024
    implementation_string = '%.2f' % implementation_size
    Unused_percent = (Unused_KB/implementation_size)*100
    Unused_percent_string = '%.2f' % Unused_percent
    Waste_cost = .07*Unused_KB
    Waste_string = '%.2f' % Waste_cost
    Unused_blocks = int((Unused_percent/100)*num_blocks)
    CPI_int = cycle_total/intruction_count
    CPI_string = '%.2f' % CPI_int
    print (hit_rate_string + '%')
    print (miss_rate_string + '%')
    print ('{:24}'.format('CPI: ') + CPI_string + ' Cycles/Instruction')
    print ('{:24}'.format('Unused Cache Space: ') + Unused_string + 'KB / ' + implementation_string + 'KB = ' + Unused_percent_string + '%  Waste: $' + Waste_string)
    print ('{:24}'.format('Unused Cache Blocks: ') + str(Unused_blocks) + ' / ' + str(num_blocks))
