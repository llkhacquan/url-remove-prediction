# this tool pre-process raw data to train-able data
# usage: python3 prepage_data.py <input.gz> <output.gz>
# input:
#   input.gz: each line contains <label> <url>;
#   label = 'true' if the url was removed by mcf; else it's 'false'
#
# output
#   output.gz: each line contains:
#       <label> <url> <host> <host_hash> <hash_1> <hash_2> <hash_3> .. <hash_30>
#       label = true|false
#       url = origin url
#       host = host of given url
#       host_hash = hash of given host
#       hash_* = hashes of components of url's path; see implemetation for details


import logging
import sys
import os
import re
import gzip

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')


def my_hash(s):
    return str(hash(s))


def processing_a_line(line):
    label, url = line.strip().split(' ')
    # split url by '/' and remove the first 2 parts
    parts = re.split('/', url)[2:]
    host = parts[0]
    parts = parts[1:]
    parts2 = []
    result = label + ' ' + url + ' ' + host + ' ' + my_hash(host) + ' '
    for part in parts:
        t = re.split('[\?\&\.=\-\+]', part)
        parts2 += t
    count = 0
    for part in parts2:
        result += my_hash(part) + ' '
        count += 1
        if (count >= 30):
            break

    # ensure each line always have 34 parts
    missing = 34 - len(result.split())
    for i in range(missing):
        result += '0 '
    return result.strip()


def pre_process_data(input_file, output_file):
    logging.info('Processing ' + str(input_file) + ' to '+str(output_file))

    if (not output_file.endswith('.gz')):
        output_file += '.gz'
    out = gzip.open(output_file, 'wt')

    count = 0
    input = gzip.open(input_file, 'rt')
    for line in input:
        processed_line = processing_a_line(line)
        out.write(processed_line + '\n')
        count += 1
        if (count % 100000 == 0):
            logging.info('processed ' + str(count) + ' lines')
    logging.info('Done - processed ' + str(count) + ' lines')


pre_process_data(sys.argv[1], sys.argv[2])

processing_a_line('true https://example.com')
processing_a_line('true https://example.com/')
processing_a_line('true https://example.com/hello')
processing_a_line('true https://example.com/hello/abc/')
processing_a_line('true https://example.com/hello/abc/?q=123&c=342')
