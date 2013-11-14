#!/usr/bin/python
# -*- coding: utf-8 -*-

import simplejson
import argparse
import subprocess
import sys
import time

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

def check_once(conf):
    result = simplejson.loads(subprocess.check_output(['nc', conf['host'], str(conf['port'])]).strip())
    return result
    
def compare_results(trial1, trial2):
    errors = {}
    error_clusters = {}
    for key1 in trial2:
        level_1_item = trial2[key1]
        if isinstance(level_1_item, dict):
            for key2 in level_1_item: #cluster
                level_2_item = level_1_item[key2]
                if isinstance(level_2_item, dict): #server
                    if int(level_2_item['server_connections']) > 0 or \
                    (int(level_2_item['requests']) - int(trial1[key1][key2]['requests'])) == 0:
                        continue
                    errors[key2] = 1
                    error_clusters[key1] = 1
                    
    problem = None
    rv = 0
    if error_clusters:
        problem = 'error with redis cluster: %s\nproblem shards: %s' \
        % (','.join(error_clusters.keys()), ','.join(errors.keys()))
        rv = 1
    return problem, rv

def check(conf):
    trail1 = check_once(conf)
    time.sleep(2)
    trail2 = check_once(conf)
    return compare_results(trail1, trail2)
    
if __name__ == '__main__':
    conf = {
        'host': '',
        'port': 22222,
    }
    description = '''Python version of https://github.com/wanelo/nagios-checks/blob/master/check_twemproxy'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("host", help="Host name or IP address")
    parser.add_argument("-P", "--port", help="Port")
    args = parser.parse_args()
    conf['host'] = args.host
    if args.port:
        conf['port'] = int(args.port)
    
    problem, _ = check(conf)
    
    if problem is None:
        print 'TWEMPROXY OK : %s' % conf['host']
        sys.exit(STATE_OK)
    else:
        print 'TWEMPROXY CRITICAL : %s\n%s' % (conf['host'], problem)
        sys.exit(STATE_CRITICAL)
