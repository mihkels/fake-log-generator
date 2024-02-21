#!/usr/bin/python
import argparse
import datetime
import gzip
import random
import sys
import time

import numpy as np
from faker import Faker
from tzlocal import get_localzone

import log_write_sleep

local = get_localzone()


# todo:
# allow writing different patterns (Common Log, Apache Error log etc)
# log rotation

parser = argparse.ArgumentParser(__file__, description="Fake Apache Log Generator")
parser.add_argument("--output", "-o", dest='output_type', help="Write to a Log file, a gzip file or to STDOUT",
                    choices=['LOG', 'GZ', 'CONSOLE'])
parser.add_argument("--num", "-n", dest='num_lines', help="Number of lines to generate (0 for infinite)", type=int,
                    default=1)
parser.add_argument("--prefix", "-p", dest='file_prefix', help="Prefix the output file name", type=str)
parser.add_argument("--sleep", "-s", help="Sleep this long between lines (in seconds)", default=0.0, type=float)

parser.add_argument('--output-dir', '-d', help='Output directory for log files', default="", type=str)
parser.add_argument('--filename', '-f', help='Log file name', default="", type=str)
parser.add_argument('--min-delay', help='Minimum delay between writes in milliseconds', default=0, type=int)
parser.add_argument('--max-delay', help='Maximum delay between writes in milliseconds', default=0, type=int)

args = parser.parse_args()

log_lines = args.num_lines
file_prefix = args.file_prefix
output_type = args.output_type
min_write_delay = args.min_delay
max_write_delay = args.max_delay
output_filename = args.filename
output_dir = log_write_sleep.write_log_directory(args.output_dir)

faker = Faker()

timestr = time.strftime("%Y%m%d-%H%M%S")
otime = datetime.datetime.now()

if output_filename == '':
    outFileName = (
        f'{file_prefix}_access_log_{timestr}.log' if file_prefix else f'access_log_{timestr}.log'
    )
else:
    outFileName = f'{output_filename}.log'

outFileName = output_dir + outFileName
print(f'Output file: {outFileName}')

match output_type:
    case 'LOG':
        f = open(outFileName, 'a')
    case 'GZ':
        f = gzip.open(f'{outFileName}.gz', 'w')
    case 'CONSOLE':
        # TODO: Add implementation
        pass
    case _:
        f = sys.stdout

response = ["200", "404", "500", "301"]

verb = ["GET", "POST", "DELETE", "PUT"]

resources = ["/list", "/wp-content", "/wp-admin", "/explore", "/search/tag/list", "/app/main/posts",
             "/posts/posts/explore", "/apps/cart.jsp?appID="]

ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

rng = np.random.default_rng(seed=int(time.time()))

flag = True
while flag:
    write_sleep = log_write_sleep.write_sleep(min_write_delay, max_write_delay)
    if write_sleep != 0:
        time.sleep(write_sleep / 1000)

    if args.sleep:
        increment = datetime.timedelta(seconds=args.sleep)
    else:
        increment = datetime.timedelta(seconds=random.randint(30, 300))
    otime += increment

    ip = faker.ipv4()
    dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
    tz = datetime.datetime.now(local).strftime('%z')
    vrb = rng.choice(verb, p=[0.6, 0.1, 0.1, 0.2])

    uri = random.choice(resources)
    if uri.find("apps") > 0:
        uri += repr(random.randint(1000, 10000))

    resp = rng.choice(response, p=[0.9, 0.04, 0.02, 0.04])
    byt = int(random.gauss(5000, 50))
    referer = faker.uri()
    useragent = rng.choice(ualist, p=[0.5, 0.3, 0.1, 0.05, 0.05])()
    f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"\n' % (ip, dt, tz, vrb, uri, resp, byt, referer, useragent))

    log_lines = log_lines - 1
    flag = log_lines != 0
    if args.sleep:
        time.sleep(args.sleep)
